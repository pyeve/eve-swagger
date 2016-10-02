import json


if __name__ == '__main__':
    import sys
    import os
    import unittest
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..')))

from eve_swagger.tests import TestBase  # noqa: E402


class TestEveSwagger(TestBase):
    def test_api(self):
        self.app.debug = True
        r = self.test_client.get('/api-docs')
        self.assertEqual(r.status_code, 200)

    def test_json(self):
        self.app.debug = True
        r = self.test_client.get('/api-docs')
        s = r.get_data().decode('utf-8')  # raises UnicodeError
        json.loads(s)  # raises ValueError

    def test_doc_is_dict(self):
        doc = self.swagger_doc
        self.assertIsInstance(doc, dict)

    def test_info(self):
        doc = self.swagger_doc

        self.assertIn('info', doc)
        self.assertIn('title', doc['info'])
        self.assertTrue(isinstance(doc['info']['title'], u''.__class__))
        self.assertIn('version', doc['info'])
        self.assertTrue(isinstance(doc['info']['version'], u''.__class__))

    def test_paths(self):
        doc = self.swagger_doc
        url = self.domain['people']['url']
        item_title = self.domain['people']['item_title']

        self.assertIn('paths', doc)
        self.assertIsInstance(doc['paths'], dict)
        self.assertIn('/'+url, doc['paths'])
        self.assertIn('/%s/{%sId}' % (url, item_title.lower()), doc['paths'])

    def test_definitions(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertIn('definitions', doc)
        self.assertIsInstance(doc['definitions'], dict)
        self.assertIn(item_title, doc['definitions'])
        self.assertIn('properties', doc['definitions'][item_title])
        self.assertEqual(
            set(doc['definitions'][item_title]['properties'].keys()),
            set(['name', 'job', '_id']))

    def test_parameters_people(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        lookup_field = self.domain['people']['item_lookup_field']

        self.assertIn('parameters', doc)
        self.assertIn(item_title+'_'+lookup_field, doc['parameters'])

    def test_resource_description(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertEqual('the people resource',
                         doc['definitions'][item_title]['description'])

    def test_field_description(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        props = doc['definitions'][item_title]['properties']

        self.assertEqual('the last name of the person',
                         props['name']['description'])

    def test_disabled_resource(self):
        doc = self.swagger_doc
        url = self.domain['disabled_resource']['url']
        item_title = self.domain['disabled_resource']['item_title']
        lookup_field = self.domain['disabled_resource']['item_lookup_field']

        self.assertNotIn('/'+url, doc['paths'])
        self.assertNotIn('/%s/{%sId}' % (url, item_title.lower()),
                         doc['paths'])
        self.assertNotIn(item_title, doc['definitions'])
        self.assertNotIn(item_title+'_'+lookup_field, doc['parameters'])

    def test_data_relation_source_field(self):
        doc = self.swagger_doc

        source_field = self.domain['people']['item_title']+'_job'
        self.assertIn(source_field, doc['definitions'])

    def test_reference_to_data_relation_source_field(self):
        doc = self.swagger_doc
        people_it = self.domain['people']['item_title']
        people_props = doc['definitions'][people_it]['properties']
        dr_1_it = self.domain['dr_resource_1']['item_title']
        dr_1_props = doc['definitions'][dr_1_it]['properties']
        key = people_it + '_job'

        self.assertIn('$ref', people_props['job'])
        self.assertEqual('#/definitions/%s' % key,
                         people_props['job']['$ref'])

        self.assertIn('$ref', dr_1_props['copied_field_with_description'])
        self.assertEqual('#/definitions/%s' % key,
                         dr_1_props['copied_field_with_description']['$ref'])

    def test_data_relation_extended_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_1']['item_title']
        lookup_field = self.domain['dr_resource_1']['item_lookup_field']
        par = doc['parameters'][item_title+'_'+lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'foobar copied_field (links to {0}_job)'.format(people_it),
            par['description'])

    def test_data_relation_copied_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_2']['item_title']
        lookup_field = self.domain['dr_resource_2']['item_lookup_field']
        par = doc['parameters'][item_title+'_'+lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'the job of the person (links to {0}_job)'.format(people_it),
            par['description'])


if __name__ == '__main__':
    unittest.main()
