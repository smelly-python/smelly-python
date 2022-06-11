import re
import requests
from bs4 import BeautifulSoup

DOCUMENTATION_URLS = [
    'https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html',
    'https://pylint.pycqa.org/en/latest/user_guide/checkers/extensions.html'
]

explanations = None


def _get_explanation_headers(url):
    # TODO: fix if no internet
    res = requests.get(url)
    soup = BeautifulSoup(res.content, features='html.parser')
    return [*soup.findAll('dt', {'class': 'field-even'}), *soup.findAll('dt', {'class': 'field-odd'})]


def initialize():
    """
    Initializes the explanation dictionary by loading the documentation pages.
    """
    global explanations
    explanations = dict()

    explanation_headers = [header for url in DOCUMENTATION_URLS for header in _get_explanation_headers(url)]

    for header in explanation_headers:
        code = re.search(r'([A-Z]\d+)', header.text).group(1)
        explanation = next(header.find_next('dd').children)
        # Remove message itself from the explanation
        next(explanation.children).extract()
        explanations[code] = str(explanation)


def get_explanation(code: str) -> str:
    """
    Returns the html element as string of the explanation that correspond to the given smell
    :param code: the code (like E1234) of the smell.
    :return: the explanation
    """
    # TODO: Handle this error somewhere
    #  -> probably just a message saying that no explanations are added
    if explanations is None:
        raise RuntimeError('Explanations are not initialised, '
                           'perhaps the documentation could not be loaded.')
    # TODO: Handle this, also message but now that this error is not supported
    if code not in explanations:
        raise RuntimeError(f'Explanation with code {code} is not supported.')
    return explanations[code]
