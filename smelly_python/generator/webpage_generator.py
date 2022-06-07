from dominate import document
from dominate.tags import *
from os import path


def generate_webpage():
    doc = document(title='Smelly Python code smell report')

    with open(path.join(path.dirname(__file__), '../resources/style.css'), 'r', encoding='utf-8') as style_file:
        with doc.head:
            style(style_file.read())

    with doc:
        h1('Smelly Python')

    return str(doc)
