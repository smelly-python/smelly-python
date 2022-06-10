"""
The md generator module provides the method that generates the md comment given a list of
style errors.
"""
from os import path

from smelly_python.generator.webpage_generator import get_html_path


def get_block(string):
    """
    Gets a string as an MD block.
    :param: string the string to format
    :return: the string as an MD block
    """
    return string + '\n\n'


def get_link(label, url):
    """
    Formats a link to MD format.
    :param: label the label to use for the link
    :url: the url the link should point to
    :return: the link in MD format
    """
    return '[' + label + '](' + url + ')'


def get_table(headers, data):
    """
    Creates an MD table from headers and data.
    :param: headers the headers of the table
    :data: the data to go in the table
    :return: the table in MD format
    """
    # fix headers to use at least one character
    headers = [' ' if header == '' else header for header in headers]

    table = ''
    # header
    table += '| ' + ' | '.join(headers) + ' |\n'
    # line
    table += '|' + '|'.join(['-' * (len(header) + 2) for header in headers]) + '|\n'
    # data
    for smell in data:
        table += '| ' + ' | '.join(smell) + ' |\n'

    # return
    return table


def get_code_smell_number_string(number):
    """
    Returns the number of code smells as a grammatically correct string.
    :param: number the number of code smells
    :return: the number of code smells as a correct string
    """
    if number < 1:
        return 'no code smells'
    if number == 1:
        return '1 code smell'
    return str(number) + ' code smells'


def generate_md(report, output_path='report/smelly_python'):
    """
    Generate the MD file that will become the GitHub comment.
    :param: report the object holding the data to report
    :param: output_path the path to output to
    """
    result = ''

    # title
    result += get_block(f'# Smelly Python: {report.grade}/10')

    # summary
    result += get_block(
        '> Smelly Python found '
        + get_link(
            get_code_smell_number_string(len(report.code_smells)),
            'smelly_python/index.html'
        )
        + ' in your project.'
    )

    if report.is_clean():
        # congratulations
        result += get_block('Good job! :partying_face:')

    else:
        # table
        headers = ['', 'File', 'Lines', 'Smell']
        data = [[
            # emoji matching the priority
            smell.type.value,
            # link to the relevant file
            get_link(
                smell.location.path,
                path.join(output_path, get_html_path(smell.location.path))
            ),
            # location in the file
            str(smell.location.line) + (
                ':' + str(smell.location.column) if smell.location.column != 0 else ''
            ),
            # the symbol converted to a readable string
            smell.get_readable_symbol()
        ] for smell in report.code_smells]
        result += get_block(get_table(headers, data))

    # export
    with open(path.join(output_path, 'comment.md'), 'w', encoding='utf-8') as index:
        index.write(result)
