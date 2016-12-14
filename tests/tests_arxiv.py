import unittest
from hypothesis import given
import hypothesis.strategies as st
from arcas.arXiv.main import Arxiv

arxiv_entry = st.fixed_dictionaries(
                   {'{http://arxiv.org/schemas/atom}affiliation': st.text(
                       min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}author': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}category': st.booleans(),
                    '{http://arxiv.org/schemas/atom}comment': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}doi': st.text(min_size=5,
                                                                  max_size=20),
                    '{http://arxiv.org/schemas/atom}entry': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}id': st.text(min_size=5,
                                                                 max_size=20),
                    '{http://arxiv.org/schemas/atom}journal_ref': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}link': st.booleans(),
                    '{http://arxiv.org/schemas/atom}name': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}primary_category':
                        st.lists(st.text(min_size=5, max_size=20)),
                    '{http://arxiv.org/schemas/atom}summary': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}title': st.text(
                        min_size=5, max_size=20),
                    '{http://arxiv.org/schemas/atom}updated': st.text(
                        min_size=5, max_size=20)
                    })

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(),
                     '-t': st.text(),
                     '-b': st.text(),
                     '-r': st.text(),
                     '-s': st.text()
                     })


class TestArxiv(unittest.TestCase):

    def setUp(self):
        self.api = Arxiv()

    @given(arxiv_entry)
    def test_to_json(self, entry):

        entry['{http://arxiv.org/schemas/atom}published'] = '12-12-2016'
        post = self.api.to_json(entry)
        self.assertEqual(sorted(post.keys()), sorted(self.api.keys()))

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('au:{}'.format(arguments['-a']), parameters[0])
        self.assertEqual('ti:{}'.format(arguments['-t']), parameters[1])
        self.assertEqual('abs:{}'.format(arguments['-b']), parameters[2])
        self.assertEqual('max_results={}'.format(arguments['-r']),
                         parameters[3])
        self.assertEqual(('start={}'.format(arguments['-s'])), parameters[4])
