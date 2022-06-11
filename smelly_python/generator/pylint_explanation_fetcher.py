"""
Module to scrape the documentation of code smells from the documentation pages of pylint.
"""
import re
import requests
from bs4 import BeautifulSoup
from dominate.tags import a
from dominate.util import raw
from requests import ConnectionError as RequestError


class Explanation:
    """
    Object that contains the text of an explanation and the url to the documentation page.
    """

    def __init__(self, header=None, doc_url=None):
        if header is None or doc_url is None:
            self.html = ['-']
            self.url = None
            return
        code = re.search(r'\(([A-Z]\d+)\)', header.text)
        if code is None:
            raise ValueError('No code can be found in the message id.')
        code = code.group(1)
        explanation = next(header.find_next('dd').children)
        # Remove message itself from the explanation
        next(explanation.children).extract()
        self.code = code
        self.html = explanation.contents
        self.url = f'{doc_url}#{header.find_previous("section").attrs["id"]}'

    def to_html(self):
        """
        Converts this Explanation to a list of Dominate html elements
        that can be placed in the table.
        :return: list of Dominate html elements
        """
        raw_html = [raw(tag) for tag in self.html]
        return [*raw_html, ' ', a('[source]', href=self.url, target='_blank')]\
            if self.url is not None else raw_html

    def to_markdown(self):
        """
        Converts this Explanation to a markdown formatted string.
        :return: markdown string
        """
        text = ''.join(self.html).lstrip().replace('\n', ' ')
        return f'{text} [\\[source\\]]({self.url})' if self.url is not None else text


class ExplanationFetcher:
    """
    Fetches all explanations from the known documentation pages.
    """

    DOCUMENTATION_URLS = [
        'https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html',
        'https://pylint.pycqa.org/en/latest/user_guide/checkers/extensions.html'
    ]

    def __init__(self):
        self.explanations = {}

        try:
            explanation_headers = [(header, url) for url in self.DOCUMENTATION_URLS for header in
                                   ExplanationFetcher._fetch_explanation_headers(url)]
            for header, url in explanation_headers:
                try:
                    explanation = Explanation(header, url)
                    self.explanations[explanation.code] = explanation
                except ValueError:
                    continue
        except RequestError:
            print('Could not load the documentation page. '
                  'No additional explanations will be shown.')
            self.explanations = {}

    def get_explanation(self, code: str) -> Explanation:
        """
        Returns the html element as string of the explanation that correspond to the given smell
        :param code: the code (like E1234) of the smell.
        :return: the explanation, or an empty string if none could be found
        """
        if code not in self.explanations:
            if self.has_explanations():
                print(f'Extra documentation for the code smell with id {code} is not supported.')
            return Explanation()
        return self.explanations[code]

    def has_explanations(self) -> bool:
        """
        Returns whether the dictionary with explanations has been initialized.
        :return: true iff the explanation dictionary has values.
        """
        return len(self.explanations) != 0

    @staticmethod
    def _fetch_explanation_headers(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, features='html.parser')
        return [*soup.findAll('dt', {'class': 'field-even'}),
                *soup.findAll('dt', {'class': 'field-odd'})]
