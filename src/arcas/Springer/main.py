from arcas.tools import Api
from .api_key import api_key
from xml.etree import ElementTree


class Springer(Api):
    """
     API argument is 'springer'.
    """
    def __init__(self):
        self.standard = 'http://api.springer.com/metadata/pam?q='
        self.key_api = api_key

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 's=' in i or 'p=' in i:
                url += '&{}'.format(i)
            else:
                url += '+AND+{}'.format(i)
        url += '&api_key={}'.format(self.key_api)
        return url

    def to_json(self, article):
        """A function which takes a dictionary with structure of the Springer
        results and transform it to a standardized format.
        """
        old_keys = list(article.keys())
        for i in old_keys:
            keep = i.split('}')
            article[keep[-1]] = article.pop(i)

        article['author'], article['key_word'] = [], []

        for i in article['creator'].split(','):
            article['author'].append({'name': i})

        article['date'] = {
                'year': int(article['publicationDate'].split('-')[0])}
        try:
            article['abstract'] = article.pop('p')
        except KeyError:
            article['abstract'] = "Empty Results "
        article['journal'] = article.pop('publicationName')
        article['pages'] = ""
        article['provenance'] = 'Springer'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

        return post

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()[3]
        if not parents:
            articles = False
        else:
            articles = [{}]
            for obj in parents.iter():
                if obj.tag.split('}')[-1] == 'article':
                    articles.append({})
                else:
                    if obj.tag in articles[-1].keys() and obj.text is None:
                        articles[-1][obj.tag] += ' ' + obj.text
                    else:
                        if obj.text is None:
                            articles[-1].update({obj.tag: obj.text})
            del articles[0]

        return articles

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('name:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('title:{}'.format(arguments['-t']))
        if arguments['-y'] is not None:
            parameters.append('year:{}'.format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('s={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('p={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root


