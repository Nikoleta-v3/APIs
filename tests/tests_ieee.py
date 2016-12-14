import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.IEEE.main import Ieee

ieee_entry = st.fixed_dictionaries(
                  {'title': st.text(min_size=5, max_size=20),
                   'authors': st.text(min_size=5, max_size=20),
                   'affiliations': st.text(min_size=5, max_size=20),
                   'term': st.text(min_size=5, max_size=10),
                   'term': st.text(min_size=5, max_size=10),
                   'pubtitle': st.text(min_size=5, max_size=20),
                   'punumber': st.text(min_size=5, max_size=5),
                   'spage': st.text(max_size=3),
                   'epage': st.text(max_size=3),
                   'publisher': st.text(min_size=5, max_size=10),
                   'abstract': st.text(min_size=5, max_size=30),
                   'issn': st.text(min_size=5, max_size=10),
                   'doi': st.text(min_size=5, max_size=10),
                   'publicationId': st.text(min_size=5, max_size=10),
                   'partnum': st.text(min_size=5, max_size=10),
                   'mdurl': st.text(min_size=5, max_size=10),
                   'pdf': st.text(min_size=5, max_size=10)})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=10),
                     '-t': st.text(min_size=5, max_size=10),
                     '-b': st.text(min_size=5, max_size=10),
                     '-y': st.text(min_size=5, max_size=10),
                     '-r': st.text(min_size=5, max_size=10),
                     '-s': st.text(min_size=5, max_size=10)
                     })


class TestIEEE(unittest.TestCase):
    def setUp(self):
        self.api = Ieee()

    @given(ieee_entry)
    def test_to_json(self, entry):

        entry['py'] = '2016'

        post = self.api.to_json(entry)
        self.assertEqual(sorted(post.keys()), sorted(self.api.keys()))

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('au={}'.format(arguments['-a']), parameters[0])
        self.assertEqual('ti={}'.format(arguments['-t']), parameters[1])
        self.assertEqual('ab={}'.format(arguments['-b']), parameters[2])
        self.assertEqual('py={}'.format(arguments['-y']), parameters[3])
        self.assertEqual('hc={}'.format(arguments['-r']),
                         parameters[4])
        self.assertEqual(('rs={}'.format(arguments['-s'])), parameters[5])
