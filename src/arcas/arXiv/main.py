from arcas.tools import Api
from xml.etree import ElementTree


class Arxiv(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    def to_json(self, article):
        """A function which takes a dictionary with structure of the arXiv
        results and transform it to a standardized format.
        """
        old_keys = list(article.keys())
        for i in old_keys:
            keep = i.split('}')
            article[keep[-1]] = article.pop(i)

        article['author'], article['key_word'] = [], []

        for i in article['name'].split(','):
            article['author'].append({'name': i})
        article['date'] = {'year': int(article['published'].split('-')[0])}
        try:
            article['journal'] = article.pop('journal_ref')
        except:
            article['journal'] = "arXiv"
        try:
            if article['primary_category']:
                for i in article['primary_category']:
                    article['key_word'].append({'key_word': i})
        except:
            pass

        article['abstract'] = article.pop('summary')
        article['pages'] = ""
        article['provenance'] = 'arXiv'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

        return post

    def parse(self, root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        articles = []
        for _ in range(7):
            parents.remove(parents[0])
        if not parents:
            articles = False
        else:
            for record in parents:
                articles.append(self.xml_to_dict(record))
        return articles

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('au:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('ti:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('abs:{}'.format(arguments['-b']))
        if arguments['-r'] is not None:
            parameters.append('max_results={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('start={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root
