import unittest
from hypothesis import given
import hypothesis.strategies as st
from arcas.nature.main import Nature

nature_entry = st.fixed_dictionaries({
                     '{http://prismstandard.org/namespaces/pam/2.0/}message'
                     : st.text(min_size=5, max_size=10),
                     '{http://prismstandard.org/namespaces/pam/2.0/}article'
                     : st.text(min_size=5, max_size=10),
                     '{http://www.w3.org/1999/xhtml}head': st.text(
                         min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}identifier'
                     : st.text(min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}title': st.text(
                         min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}creator': st.text(
                         min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}creator': st.text(
                         min_size=5, max_size=10),
                     '{http://prismstandard.org/namespaces/basic/2.1'
                     '/}publicationName': st.text(min_size=5, max_size=10),
                     '{http://prismstandard.org/namespaces/basic/2.1/}eIssn'
                     : st.text(min_size=5, max_size=10),
                     '{http://prismstandard.org/namespaces/basic/2.1/}doi'
                     : st.text(min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}publisher': st.text(
                         min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}subject': st.text(
                         min_size=5, max_size=10),
                     '{http://purl.org/dc/elements/1.1/}description': st.text(
                         min_size=5, max_size=20)
})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=10),
                     '-t': st.text(min_size=5, max_size=10),
                     '-b': st.text(min_size=5, max_size=10),
                     '-y': st.text(min_size=5, max_size=10),
                     '-r': st.text(min_size=5, max_size=10),
                     '-s': st.text(min_size=5, max_size=10)
                     })


class TestNature(unittest.TestCase):
    def setUp(self):
        self.api = Nature()

    @given(nature_entry)
    def test_to_json(self, entry):
        entry['{http://prismstandard.org/namespaces/basic/2.1'
                     '/}publicationDate'] = '2016-01-01'
        post = self.api.to_json(entry)
        self.assertEqual(sorted(post.keys()), sorted(self.api.keys()))

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('dc.creator={}'.format(arguments['-a']), parameters[0])
        self.assertEqual('dc.title adj {}'.format(arguments['-t']),
                         parameters[1])
        self.assertEqual('dc.description adj {}'.format(arguments['-b']),
                         parameters[2])
        self.assertEqual('prism.publicationDate={}'.format(arguments['-y']),
                         parameters[3])
        self.assertEqual('maximumRecords={}'.format(arguments['-r']),
                         parameters[4])
        self.assertEqual(('startRecord={}'.format(arguments['-s'])),
                         parameters[5])




