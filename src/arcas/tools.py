from xml.etree import ElementTree
from collections import defaultdict

import json
import requests
import hashlib
from ratelimit import *


class APIError(Exception):
    """An API Error Exception."""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class Api():

    def __init__(self, standard):
        """Initializations"""
        self.standard = standard

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            url += '&{}'.format(i)
        return url

    @staticmethod
    @rate_limited(3)
    def make_request(url):
        """Request from an API and returns response."""
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise APIError(response.status_code)
        return response

    @staticmethod
    def xml_to_dict(branch):
        """Branch to dictionary"""
        article = defaultdict()
        for at in branch.iter():
            if at.tag in article and at.text is not None:
                article[at.tag] += ',{}'.format(at.text)
            else:
                article.update({at.tag: at.text})
        return article

    @staticmethod
    def keys():
        keys = ['key', 'unique_key', 'title', 'abstract', 'author', 'date',
                'journal', 'pages', 'read', 'key_word', 'provenance']
        return keys

    @staticmethod
    def to_json(article):
        pass

    @staticmethod
    def parse(root):
        pass

    @staticmethod
    def parameters_fix(arguments):
        pass

    @staticmethod
    def get_root(response):
        root = ElementTree.parse(response.raw).getroot()
        return root

    @staticmethod
    def lower_case(post):
        post = dict((k.lower() if isinstance(k, str) else k,
                     v.lower() if isinstance(v, str) else v) for k, v in
                    post.items())
        return post

    @staticmethod
    def create_keys(article):
        """Returns public key 'AuthorYear' and
        unique key hash('Author''Title''Year''Abstract')
        """
        full_name = article['author'][0]['name'].split(' ')
        year = article['date']['year']
        string = '{}{}{}{}'.format(full_name[-1], article['title'], year,
                                   article['abstract'])

        hash_object = hashlib.md5(string.encode('utf-8'))

        key = '{}{}'.format(full_name[-1], year)
        unique_key = hash_object.hexdigest()

        return key, unique_key

    def validate_post(self, arguments, post):
        """
        Checks if the query arguments abstract and title  were satisfied.

        Parameters:
            - arguments
            - post
        Returns:
            - True of False
        """
        post = self.lower_case(post)
        word = [arguments['-b'], arguments['-t']]
        for i, wr in enumerate(word):
            if wr is not None:
                word[i] = wr.lower()
        check = [post['abstract'], post['title']]
        return all([w in check[_] for _, w in enumerate(word) if w is not None])

    def run(self, url, arguments, validate):
        """Putting everything together. Creates the url, makes the request,
        transforms from xml to dict to a standardized format and output to
        json file.
        """
        response = self.make_request(url)
        root = self.get_root(response)
        articles = self.parse(root)
        if not articles:
            raise ValueError('Empty results at {}'.format(url))
        else:
            for record in articles:
                post = self.to_json(record)

                if validate is True:
                    try:
                        self.validate_post(arguments, post)
                    except:
                        string = "Query was not satisfied for article with " \
                                 "citation  key{} and unique key:{}".format(
                                  post['key'], post['unique_key'])
                        raise NotImplementedError(string)
                return post

    @staticmethod
    def export(post, filename):
        """ Write the results to a json file
        """
        with open('{}.json'.format(filename), 'a') as jsonfile:
            json.dump(post, jsonfile)


