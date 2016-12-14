import unittest
from hypothesis import given
import hypothesis.strategies as st
from arcas.Springer.main import Springer


springer_entry = st.fixed_dictionaries({
                    'records': st.text(min_size=5, max_size=10),
                    '{http://prismstandard.org/namespaces/pam/2.0/}message':
                        st.text(min_size=5, max_size=10),
                    '{http://www.w3.org/1999/xhtml}head': st.text(min_size=5,
                                                                  max_size=10),
                    '{http://prismstandard.org/namespaces/pam/2.0/}article':
                        st.text(min_size=5, max_size=10),
                    '{http://purl.org/dc/elements/1.1/}identifier': st.text(
                        min_size=5, max_size=10),
                    '{http://purl.org/dc/elements/1.1/}title': st.text(
                        min_size=5, max_size=10),
                    '{http://purl.org/dc/elements/1.1/}creator': st.text(
                        min_size=5, max_size=10),
                    '{http://purl.org/dc/elements/1.1/}creator': st.text(
                        min_size=5, max_size=10),
                    '{http://prismstandard.org/namespaces/basic/2.0/}publicationName':
                        st.text(min_size=5, max_size=10),
                    'printIsbn': st.text(min_size=5, max_size=10),
                    'electronicIsbn': st.text(min_size=5, max_size=10),
                    '{http://purl.org/dc/elements/1.1/}publisher': st.text(
                        min_size=5, max_size=10),
                    '{http://www.w3.org/1999/xhtml}body':
                        st.text(min_size=5, max_size=10),
                    'h1': st.text(min_size=5, max_size=10),
                    'p': st.text(min_size=5, max_size=20)})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=10),
                     '-t': st.text(min_size=5, max_size=10),
                     '-b': st.text(min_size=5, max_size=10),
                     '-y': st.text(min_size=5, max_size=10),
                     '-r': st.text(min_size=5, max_size=10),
                     '-s': st.text(min_size=5, max_size=10)
                     })


class TestSpinger(unittest.TestCase):
    def setUp(self):
        self.api = Springer()

    @given(springer_entry)
    def test_to_json(self, entry):

        entry["{http://prismstandard.org/namespaces/basic/2.0' \
              '/}publicationDate"] = '2017-01-01'
        post = self.api.to_json(entry)
        self.assertEqual(sorted(post.keys()), sorted(self.api.keys()))

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('name:{}'.format(arguments['-a']), parameters[0])
        self.assertEqual('title:{}'.format(arguments['-t']),
                         parameters[1])
        self.assertEqual('year:{}'.format(arguments['-y']),
                         parameters[2])
        self.assertEqual('s={}'.format(arguments['-r']),
                         parameters[3])
        self.assertEqual(('p={}'.format(arguments['-s'])),
                         parameters[4])
