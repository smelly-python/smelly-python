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
            # Count number of nested folders by counting /
            link_to_home = '/'.join('..' for _ in range(file[0].location.path.count('/'))) + '/'
            h4(a('Home', href=link_to_home), f' > {file[0].location.path}')

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


def get_html_path(file):
    """
    Gets the html path of a file.
    :param: file the path to the file
    :return: the html path to the file
    """
    return Path(file).with_suffix('.html')


def generate_webpage(report, output_path=path.join('report', 'smelly_python')):
    """
    Generates the webpage showing the errors as a string.
    :return: the html webpage as a string
    """
    _create_output(output_path)

    doc = document(title='Smelly Python code smell report')

    with doc.head:
        link(rel='stylesheet', href='style.css')

    code_smell_by_file = report.group_by_file()
    html_paths = {
        file: get_html_path(file)
        for file in [file[0].location.path for file in code_smell_by_file]
    }

    with doc:
        h1('Smelly Python')
        h4(f'Your project scored {report.grade}/10')
        with div():
            with table():
                with thead():
                    row = tr()
                    row += th('Severity')
                    row += th('File')
                    row += th('Code smell')
                    row += th('Message')
                    row += th('Location')
                with tbody():
                    for smell in report.code_smells:
                        file = smell.location.path
                        html_path = html_paths[file]

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
                        row += td(a(file, href=html_path))
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

        directory = path.dirname(path.join(output_path, file[0].location.path))
        os.makedirs(directory, exist_ok=True)

        html_path = Path(path.join(output_path, file[0].location.path))\
            .with_suffix('.html')
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(file_page))

    # Copy static resources
    for file in Path(path.join(path.dirname(path.dirname(__file__)), 'resources')).glob('*'):
        shutil.copy(file, output_path)

    # Create index.html
    with open(path.join(output_path, 'index.html'), 'w', encoding='utf-8') as index:
        index.write(str(doc))
