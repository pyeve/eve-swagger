if __name__ == '__main__':
    import sys
    import os
    import unittest
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 '..', '..')))

from eve_swagger.tests import TestBase

class TestFoobar(TestBase):
    def test_doc_is_dict(self):
        doc = self.swagger_doc
        self.assertIsInstance(doc, dict)

    def test_info(self):
        doc = self.swagger_doc

        self.assertIn('info', doc)
        self.assertIn('title', doc['info'])
        self.assertIsInstance(doc['info']['title'], basestring)
        self.assertIn('version', doc['info'])
        self.assertIsInstance(doc['info']['version'], basestring)

    def test_paths(self):
        doc = self.swagger_doc

        self.assertIn('paths', doc)
        self.assertIn('/'+self.domain['people']['url'], doc['paths'])
        self.assertIn('/%s/{%sId}' % (self.domain['people']['url'],
                                      self.domain['people']['item_title'].lower()),
                      doc['paths'])

    def test_resource_description(self):
        pass


if __name__ == '__main__':
    unittest.main()
