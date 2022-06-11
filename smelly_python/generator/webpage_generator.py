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
    a, footer, script, pre, code, link, h4, p
from dominate.util import raw

from smelly_python.code_smell import CodeSmell, Priority, Report
from smelly_python.generator.pylint_explanation_fetcher import ExplanationFetcher


def _create_output(output_dir):
    if path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)


def _generate_code_document(file: [CodeSmell]):
    doc = document(title='Smelly Python code smell report')

    # Count number of nested folders by counting /
    link_to_home = '/'.join('..' for _ in range(file[0].location.path.count('/'))) + '/'

    with doc.head:
        link(rel='stylesheet', href=f'{link_to_home}/style.css')
        link(rel='stylesheet', href=f'{link_to_home}/idea.min.css')

    with doc:
        h1('Smelly Python')
        with div(id=file[0].location.path):
            h4(a('Home', href=link_to_home), f' > {file[0].location.path}')

            with pre(id='code-block'):
                full_file_path = path.join(getcwd(), file[0].location.path)
                with open(full_file_path, 'r', encoding='utf-8') as code_file:
                    code(code_file.read(), _class='language-python')

        with footer():
            script(src=f'{link_to_home}/highlight.min.js')
            script(src=f'{link_to_home}/highlightjs-line-numbers.min.js')
            script('hljs.highlightAll();')
            script(src=f'{link_to_home}/script.js')
            script(raw(f'setSmells([{",".join(smell.jsonify() for smell in file)}])'))

    return doc


def get_html_path(file):
    """
    Gets the html path of a file.
    :param: file the path to the file
    :return: the html path to the file
    """
    return Path(file).with_suffix('.html')


def _create_code_page(file, output_path):
    file_page = _generate_code_document(file)

    directory = path.dirname(path.join(output_path, file[0].location.path))
    os.makedirs(directory, exist_ok=True)

    html_path = Path(path.join(output_path, file[0].location.path)) \
        .with_suffix('.html')
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(str(file_page))


def generate_webpage(report: Report, explanations = ExplanationFetcher,
                     output_path=path.join('report', 'smelly_python')):
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
        if report.is_clean():
            p('There were no code smells found. Good job!')
            # raw('There were no code smells found! <strong>Good job!</strong>')

        else:
            with div():
                with table(_class='smells_table'):
                    with thead():
                        row = tr()
                        row += th('Severity')
                        row += th('File')
                        row += th('Code smell')
                        row += th('Message')
                        row += th('Location')
                    with tbody():
                        for smell in report.code_smells:
                            html_path = html_paths[smell.location.path]

                            row = tr(_class='center-text')
                            table_data = td()
                            if smell.type == Priority.ERROR:
                                table_data.add(image(src='error.svg', alt='error'))
                            elif smell.type == Priority.WARNING:
                                table_data.add(image(src='warning.svg', alt='warning'))
                            else:
                                # Will be "refactor" or "convention"
                                table_data.add(image(src='info.svg', alt='info'))

                            row += table_data
                            row += td(a(smell.location.path, href=html_path))
                            row += td(smell.symbol)
                            row += td(smell.message)
                            line_num = smell.location.line
                            code_smell_link = f'{html_path}#line-' \
                                              f'{str(line_num - 3 if line_num > 3 else line_num)}'
                            row += td(a(f'{smell.location.line}:{smell.location.column}',
                                        href=code_smell_link))
                            row += td(*explanations.get_explanation(smell.message_id).to_html(),
                                      _class='explanation')

        with footer():
            if not report.is_clean():
                raw('<strong>Icons by svgrepo.com</strong>')
            script(src='script.js')

    for file in code_smell_by_file:
        _create_code_page(file, output_path)

    # Copy static resources
    for file in Path(path.join(path.dirname(path.dirname(__file__)), 'resources')).glob('*'):
        shutil.copy(file, output_path)

    # Create index.html
    with open(path.join(output_path, 'index.html'), 'w', encoding='utf-8') as index:
        index.write(str(doc))
