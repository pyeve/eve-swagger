from eve_swagger.tests import TestBase


class TestFoobar(TestBase):
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

        self.assertIn('paths', doc)
        self.assertIn('/'+self.domain['people']['url'], doc['paths'])
        self.assertIn(
            '/%s/{%sId}' % (self.domain['people']['url'],
                            self.domain['people']['item_title'].lower()),
            doc['paths'])

    def test_resource_description(self):
        pass
