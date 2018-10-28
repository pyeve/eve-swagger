import json
from jsonschema import validate, ValidationError


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
        self.assertIn('/' + url, doc['paths'])
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
            set(['name', 'job', 'email', 'position', '_id',
                 'relations', 'location']))

    def test_definitions_are_jsonschema(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        # validate if schema is jsonschema
        try:
            validate({}, doc['definitions'][item_title])
        except ValidationError:
            # validation errors are only thrown after schema is checked
            self.assertTrue(True)

    def test_parameters_people(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        lookup_field = self.domain['people']['item_lookup_field']

        self.assertIn('parameters', doc)
        self.assertIn(item_title + '_' + lookup_field, doc['parameters'])

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

    def test_field_example(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']
        props = doc['definitions'][item_title]['properties']

        self.assertEqual('Doe', props['name']['example'])

    def test_disabled_resource(self):
        doc = self.swagger_doc
        url = self.domain['disabled_resource']['url']
        item_title = self.domain['disabled_resource']['item_title']
        lookup_field = self.domain['disabled_resource']['item_lookup_field']

        self.assertNotIn('/' + url, doc['paths'])
        self.assertNotIn('/%s/{%sId}' % (url, item_title.lower()),
                         doc['paths'])
        self.assertNotIn(item_title, doc['definitions'])
        self.assertNotIn(item_title + '_' + lookup_field, doc['parameters'])

    def test_data_relation_source_field(self):
        doc = self.swagger_doc

        source_field = self.domain['people']['item_title'] + '_job'
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
        self.assertIn(key, doc['definitions'])

        self.assertIn('$ref', dr_1_props['copied_field_with_description'])
        self.assertEqual('#/definitions/%s' % key,
                         dr_1_props['copied_field_with_description']['$ref'])

        key = people_it + '__id'
        people_rels_props = people_props['relations']['items']['properties']
        self.assertIn('$ref', people_rels_props['relation'])
        self.assertEqual('#/definitions/%s' % key,
                         people_rels_props['relation']['$ref'])
        self.assertIn(key, doc['definitions'])

    def test_data_relation_extended_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_1']['item_title']
        lookup_field = self.domain['dr_resource_1']['item_lookup_field']
        par = doc['parameters'][item_title + '_' + lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'foobar copied_field (links to {0}_job)'.format(people_it),
            par['description'])

    def test_data_relation_copied_description(self):
        doc = self.swagger_doc
        item_title = self.domain['dr_resource_2']['item_title']
        lookup_field = self.domain['dr_resource_2']['item_lookup_field']
        par = doc['parameters'][item_title + '_' + lookup_field]
        people_it = self.domain['people']['item_title']

        self.assertIn('description', par)
        self.assertEqual(
            'the job of the person (links to {0}_job)'.format(people_it),
            par['description'])

    def test_header_parameters(self):
        doc = self.swagger_doc
        url = self.domain['people']['url']
        item_title = self.domain['people']['item_title']
        url = '/%s/{%sId}' % (url, item_title.lower())

        header_parameters = []
        # assume that header parameters are equal for PUT, PATCH, and DELETE
        for method in ['put', 'patch', 'delete']:
            for p in doc['paths'][url][method]['parameters']:
                if 'in' not in p:
                    continue
                if p['in'] == 'header':
                    if method in ['patch', 'delete']:
                        # already added in 'put'
                        self.assertIn(p, header_parameters)
                    else:
                        header_parameters += [p]

        self.assertTrue(len(header_parameters) == 1)
        h = header_parameters[0]
        self.assertIn('name', h)
        self.assertEqual(h['name'], 'If-Match')
        self.assertTrue(h['required'])

    def test_header_parameters_without_concurrency_control(self):
        url = self.domain['people']['url']
        item_title = self.domain['people']['item_title']
        url = '/%s/{%sId}' % (url, item_title.lower())

        def get_etag_param(doc):
            params = doc['paths'][url]['delete']['parameters']
            return next(p for p in params if p.get('name') == 'If-Match')

        self.app.config['IF_MATCH'] = False
        etag_param = get_etag_param(self.get_swagger_doc())
        self.assertFalse(etag_param['required'])

        self.app.config['IF_MATCH'] = True
        self.app.config['ENFORCE_IF_MATCH'] = False
        etag_param = get_etag_param(self.get_swagger_doc())
        self.assertFalse(etag_param['required'])

    def test_cors_without_origin(self):
        self.app.config['X_DOMAINS'] = ['http://example.com']
        self.app.config['X_HEADERS'] = ['Origin', 'X-Requested-With',
                                        'Content-Type', 'Accept']
        self.app.config['X_MAX_AGE'] = 2000
        r = self.test_client.get('/api-docs')

        self.assertEqual(r.status_code, 200)
        self.assertNotIn('Access-Control-Allow-Origin', r.headers)
        self.assertNotIn('Access-Control-Allow-Headers', r.headers)
        self.assertNotIn('Access-Control-Allow-Methods', r.headers)
        self.assertNotIn('Access-Control-Max-Age', r.headers)
        self.assertNotIn('Access-Control-Expose-Headers', r.headers)

    def test_cors_with_origin(self):
        self.app.config['X_DOMAINS'] = 'http://example.com'
        self.app.config['X_HEADERS'] = ['Origin', 'X-Requested-With',
                                        'Content-Type', 'Accept']
        self.app.config['X_MAX_AGE'] = 2000
        r = self.test_client.get('/api-docs',
                                 headers={'Origin': 'http://example.com'})

        self.assertEqual(r.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', r.headers)
        self.assertEqual(r.headers['Access-Control-Allow-Origin'],
                         'http://example.com')
        self.assertIn('Access-Control-Allow-Headers', r.headers)
        self.assertEqual(
            set(r.headers['Access-Control-Allow-Headers'].split(', ')),
            set(['Origin', 'X-Requested-With', 'Content-Type', 'Accept']))
        self.assertIn('Access-Control-Allow-Methods', r.headers)
        self.assertEqual(
            set(r.headers['Access-Control-Allow-Methods'].split(', ')),
            set(['HEAD', 'OPTIONS', 'GET']))
        self.assertIn('Access-Control-Max-Age', r.headers)
        self.assertEqual(r.headers['Access-Control-Max-Age'],
                         '2000')

    def test_tags(self):
        doc = self.swagger_doc
        item_title = self.domain['people']['item_title']

        self.assertIn('tags', doc)
        tag_names = [tag['name'] for tag in doc['tags']]
        self.assertTrue(len([n for n in tag_names if n == item_title]) == 1)

        url = '/' + self.domain['people']['url']
        for m in ['get', 'post', 'delete']:
            path_m = doc['paths'][url][m]
            self.assertIn('tags', path_m)
            self.assertIn(item_title, path_m['tags'])

        url = '/%s/{%sId}' % (self.domain['people']['url'], item_title.lower())
        for m in ['get', 'patch', 'put', 'delete']:
            path_m = doc['paths'][url][m]
            self.assertIn('tags', path_m)
            self.assertIn(item_title, path_m['tags'])

    def test_status_codes(self):
        doc = self.swagger_doc
        url = self.domain['people']['url']

        people = doc['paths']['/' + url]
        self.assertIn('200', people['get']['responses'])
        self.assertIn('201', people['post']['responses'])
        self.assertIn('204', people['delete']['responses'])

        item_title = self.domain['people']['item_title']
        person = doc['paths']['/%s/{%sId}' % (url, item_title.lower())]
        self.assertIn('200', person['get']['responses'])
        self.assertIn('200', person['patch']['responses'])
        self.assertIn('200', person['put']['responses'])
        self.assertIn('204', person['delete']['responses'])

    def test_schemes_override(self):
        self.app.config['SWAGGER_INFO']['schemes'] = ['https']
        r = self.test_client.get('/api-docs')
        self.assertEqual(r.status_code, 200)
        s = r.get_data().decode('utf-8')
        d = json.loads(s)
        self.assertEqual(d.get('schemes'), ['https'])

    def test_sub_resource_regex(self):
        url = self.domain['sub_resource']['url']
        resource_title = self.domain['sub_resource']['resource_title']

        self.assertEqual('people/<personid>/related', url)
        self.assertEqual('people/<personid>/related', resource_title)

    def test_resource_example(self):
        doc = self.swagger_doc
        item_title = self.domain['sub_resource']['item_title']

        self.assertIn('example', doc['definitions'][item_title])


class TestMetaParams(TestBase):
    def setUp(self, settings=None):
        super(TestMetaParams, self).setUp() # gee python 2 :)
        self.domain = self.app.config['DOMAIN']
        self.domain['people']['sorting'] = True
        self.domain['people']['projection'] = True
        self.domain['people']['embedding'] = True
        self.domain['people']['allowed_filters'] = ['*']
        # This is not as neat at one would expect because it only sets the "people" and not the people/peopl_id, etc ..
        # because there is no propagation of cascading parameters after init
        self.swagger_doc = self.get_swagger_doc()

    def test_meta_params(self):
        expected = [{'$ref': '#/parameters/projection'}, {'$ref': '#/parameters/embedded'},
                    {'$ref': '#/parameters/sort'}, {'$ref': '#/parameters/where'}]
        params = self.swagger_doc['paths']['/people']['get']['parameters']
        self.assertListEqual(expected, params)


if __name__ == '__main__':
    unittest.main()
