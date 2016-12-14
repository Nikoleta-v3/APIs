import unittest
import collections
import requests_mock
from hypothesis import given
import hypothesis.strategies as st
from xml.etree.ElementTree import Element
from arcas.tools import Api

keys = ['key', 'unique_key', 'title', 'abstract', 'author', 'date', 'journal',
        'pages', 'read', 'key_word', 'provenance']

article = {'title': 'A Title', 'abstract': 'The Abstract', 'date': {'year': 2016},
           'author': [{'name': 'Author'}]}


class TestTools(unittest.TestCase):

    def setUp(self):
        standard = 'http:/Search;'
        self.api = Api(standard)

    @given(st.lists(st.text(), min_size=2, max_size=5))
    def test_create_url(self, ls):
        parameters = list(ls)
        url = self.api.create_url_search(parameters)
        assert isinstance(url, str)

    @requests_mock.mock()
    @given(text=st.text())
    def test_requests(self, m, text):
        url = 'http://example.com'
        m.register_uri('GET', url, text=text)
        response = self.api.make_request(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, text)

    def test_xml_to_dict(self):
        root = Element('top')
        children = [Element('child')]
        root.extend(children)

        dummy_dict = self.api.xml_to_dict(root)
        self.assertEqual(type(dummy_dict), collections.defaultdict)

    def test_key(self):
        self.assertEqual(keys, self.api.keys())

    def test_create_keys(self):
        key, unique_key = self.api.create_keys(article)
        self.assertEqual(key, 'Author2016')
        self.assertEqual(len(unique_key), 32)
        assert isinstance(unique_key, str)

    def test_validate(self):
        arguments = dict()
        post = dict()
        arguments['-b'], arguments['-t'] = 'Abstract', 'Title'

        post['abstract'], post['title'] = 'abstract is a lot of sentences', \
                                          ' where a title is only one.'
        self.assertTrue(self.api.validate_post(arguments, post))

        arguments['-b'], arguments['-t'] = None, 'Title'
        self.assertTrue(self.api.validate_post(arguments, post))

        arguments['-b'], arguments['-t'] = 'Abstract', None
        self.assertTrue(self.api.validate_post(arguments, post))

