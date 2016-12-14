from arcas.tools import Api
from xml.etree import ElementTree
from collections import OrderedDict


class Plos(Api):
    """
     API argument is 'plot'.
    """
    def __init__(self):
        self.standard = 'http://api.plos.org/search?q='

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 'rows=' in i or 'start=' in i:
                url += '&{}'.format(i)
            else:
                url += '+AND+{}'.format(i)
        return url

    @staticmethod
    def get_authors_abstract(raw_data):
        keys = list(raw_data.keys())
        author_index = keys.index("author_display")
        abstract_index = keys.index("abstract")
        margin = keys[author_index + 1:abstract_index + 2]
        authors = [raw_data.get(key) for key in margin[:-2]]
        abstract = [raw_data.get(key) for key in margin[-1:]]
        return authors, abstract

    def to_json(self, article):
        """A function which takes a dictionary with structure of the PLOS
        results and transform it to a standardized format.
        """
        article['author'], article['key_word'], article['pages'] = [], [], []

        list_authors, article['abstract'] = self.get_authors_abstract(article)
        for i in list_authors:
            article['author'].append({'name': i})

        article['title'] = article['title_display']
        article['date'] = {'year': int(article['publication_date'].split('-')[0])}
        article['provenance'] = 'PLOS'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)
        keys = self.keys()
        keys.append('score')

        post = {key: article[key] for key in keys}

        return post

    @staticmethod
    def xml_to_dict(branch):
        """Branch to dictionary"""
        article = OrderedDict()
        for i, at in enumerate(branch.iter()):
            key = (list(at.attrib.values()) or [i])[0]
            article[key] = at.text
        return article

    def parse(self, root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        if len(parents[0]) == 0:
            articles = False
        else:
            temp = self.xml_to_dict(parents[0])
            articles = [OrderedDict()]
            for key in temp:
                if key == 'score':
                    articles[-1].update({key: temp[key]})
                    articles.append({})
                else:
                    articles[-1].update({key: temp[key]})
        return articles

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('author:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('title:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('abstract:{}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('publication_date:[{0}-01-01T00:00:00Z TO '
                              '{0}-12-30T23:59:59Z]'
                              .format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('rows={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('start={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root

