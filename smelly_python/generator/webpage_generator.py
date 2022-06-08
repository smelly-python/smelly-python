"""
The webpage generator module provides the method that generates the webpage given a list of
style errors.
"""
from os import link, path, getcwd

from dominate import document
from dominate.tags import h1, style, div, tbody, table, tr, td, thead, th, a, img, footer, script, pre, code, link, h4
from dominate.util import raw
from smelly_python.code_smell import CodeSmell


def generate_webpage(code_smells):
    """
    Generates the webpage showing the errors as a string.
    :return: the html webpage as a string
    """
    doc = document(title='Smelly Python code smell report')

    with open(path.join(path.dirname(__file__), '../resources/prism.css'), 'r', encoding='utf-8')\
            as style_file:
        with doc.head:
            style(style_file.read())

    with open(path.join(path.dirname(__file__), '../resources/style.css'), 'r', encoding='utf-8')\
            as style_file:
        with doc.head:
            style(style_file.read())
            link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-highlight/prism-line-highlight.min.css')
            link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-numbers/prism-line-numbers.min.css')


    code_smell_by_file = CodeSmell.group_by_file(code_smells)
    with doc:
        h1('Smelly Python')
        with div():
            with table():
                with thead():
                    row = tr()
                    row += th('File')
                    row += th('Code smell')
                    row += th('Message')
                    row += th('Location')
                with tbody():
                    for file in code_smell_by_file:
                        full_file_path = getcwd() + '/' + file[0].location.path
                        with tr(style='font-weight:bold'):
                            with td(colspan=4):
                                a(file[0].location.path, href=full_file_path)
                        for smell in file:
                            row = tr(_class='center-text')
                            table_data = td()
                            if smell.type == 'error':
                                table_data.add(img(src=path.join(path.dirname(__file__), '../resources/error.svg')))
                            else:
                                table_data.add(img(src=path.join(path.dirname(__file__), '../resources/warning.svg')))
                                
                            row += table_data
                            row += td(smell.symbol)
                            row += td(smell.message)
                            row += td(f'{smell.location.line}:{smell.location.column}')

        for file in code_smell_by_file:
            with div(_class='line-numbers', id=file[0].location.path):
                h4(file[0].location.path)
                data_line = ""
                # file = code_smell_by_file[0]
                for smell in file:
                    loc = smell.location
                    if loc.line == loc.end_line and loc.end_line != None:
                        data_line += f',{loc.line}'
                    else: 
                        data_line += f', {loc.line}-{loc.end_line}'

                with pre(_class='language-python', data_line=data_line):
                    full_file_path = getcwd() + '/' + file[0].location.path
                    with open(full_file_path, 'r', encoding='utf-8') as code_file:
                        code(code_file.read(), _class='language-python')
        with footer():
            raw('<strong>Icons by svgrepo.com</strong>')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/prism.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/autoloader/prism-autoloader.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-highlight/prism-line-highlight.min.js')
            script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.28.0/plugins/line-numbers/prism-line-numbers.min.js')

            with open(path.join(path.dirname(__file__), '../resources/script.js'), 'r', encoding='utf-8')\
            as file:
                script(raw(file.read()))

    return str(doc)
