"""
The webpage generator module provides the method that generates the webpage given a list of
style errors.
"""
import os
import shutil
from pathlib import Path
from os import path, getcwd

from dominate import document
from dominate.svg import image
from dominate.tags import \
    h1, div, tbody, table, tr, td, thead, th, \
    a, footer, script, pre, code, link, h4
from dominate.util import raw
from smelly_python.code_smell import CodeSmell


def _create_output(output_dir):
    if path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)


def _create_code_page(file):
    doc = document(title='Smelly Python code smell report')

    with doc.head:
        link(rel='stylesheet', href='style.css')
        link(rel='stylesheet', href='prism.css')
        link(rel='stylesheet',
             href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-highlight/'
                  'prism-line-highlight.min.css')
        link(rel='stylesheet',
             href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-numbers/'
                  'prism-line-numbers.min.css')
    with doc:
        h1('Smelly Python')
        with div(_class='line-numbers', id=file[0].location.path):
            h4(a('Home', href='./index.html'), f' > {file[0].location.path}')

            data_line = ""
            for smell in file:
                loc = smell.location
                if loc.line == loc.end_line and loc.end_line is not None:
                    data_line += f',{loc.line}'
                else:
                    data_line += f', {loc.line}-{loc.end_line}'

            with pre(id='code-block', _class='language-python', data_line=data_line):
                full_file_path = path.join(getcwd(), file[0].location.path)
                with open(full_file_path, 'r', encoding='utf-8') as code_file:
                    code(code_file.read(), _class='language-python')

        with footer():
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/prism.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/'
                       'autoloader/prism-autoloader.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/'
                       'line-highlight/prism-line-highlight.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/'
                       'line-numbers/prism-line-numbers.min.js')
            script(src='script.js')

    return doc


def generate_webpage(code_smells, output_path='output'):
    """
    Generates the webpage showing the errors as a string.
    :return: the html webpage as a string
    """
    _create_output(output_path)

    doc = document(title='Smelly Python code smell report')

    with doc.head:
        link(rel='stylesheet', href='style.css')

    code_smell_by_file = CodeSmell.group_by_file(code_smells)
    with doc:
        h1('Smelly Python')
        with div():
            with table():
                with thead():
                    row = tr()
                    row += th('Severity')
                    row += th('Code smell')
                    row += th('Message')
                    row += th('Location')
                with tbody():
                    for file in code_smell_by_file:
                        full_file_path = path.join(getcwd(), file[0].location.path)
                        html_path = Path(path.basename(full_file_path)).with_suffix('.html')
                        with tr(style='font-weight:bold'):
                            with td(colspan=4):
                                a(file[0].location.path, href=html_path)
                        for smell in sorted(file, key=lambda s: s.severity(), reverse=True):
                            row = tr(_class='center-text')
                            table_data = td()
                            if smell.type == 'error':
                                table_data.add(image(src='error.svg', alt='error'))
                            elif smell.type == 'warning':
                                table_data.add(image(src='warning.svg', alt='warning'))
                            else:
                                # Will be "refactor" or "convention"
                                table_data.add(image(src='info.svg', alt='info'))

                            row += table_data
                            row += td(smell.symbol)
                            row += td(smell.message)
                            code_smell_link = f'{html_path}#code-block.{smell.location.line}'
                            row += td(a(f'{smell.location.line}:{smell.location.column}',
                                        href=code_smell_link))

        with footer():
            raw('<strong>Icons by svgrepo.com</strong>')
            script(src='script.js')

    for file in code_smell_by_file:
        file_page = _create_code_page(file)
        html_path = Path(path.join(output_path, path.basename(file[0].location.path)))\
            .with_suffix('.html')
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(file_page))

    # Copy static resources
    for file in Path(path.join(path.dirname(path.dirname(__file__)), 'resources')).glob('*'):
        shutil.copy(file, output_path)

    # Create index.html
    with open(path.join(output_path, 'index.html'), 'w', encoding='utf-8') as index:
        index.write(str(doc))
