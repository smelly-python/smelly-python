"""
The webpage generator module provides the method that generates the webpage given a list of
style errors.
"""
from os import path
from dominate import document
from dominate.tags import h1, style


def generate_webpage():
    """
    Generates the webpage showing the errors as a string.
    :return: the html webpage as a string
    """
    doc = document(title='Smelly Python code smell report')

    with open(path.join(path.dirname(__file__), '../resources/style.css'), 'r', encoding='utf-8')\
            as style_file:
        with doc.head:
            style(style_file.read())

    with doc:
        h1('Smelly Python')

    return str(doc)
