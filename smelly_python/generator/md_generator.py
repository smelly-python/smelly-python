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
        '> Smelly Python has found '
        + get_link(str(len(report.code_smells)) + ' code smells', 'smelly_python/index.html')
        + ' in your project.'
    )

    # table
    headers = ['', 'File', 'Lines', 'Smell']
    data = [[
        smell.type.value,
        get_link(smell.location.path, path.join(output_path, get_html_path(smell.location.path))),
        str(smell.location.line) + (
            ':' + str(smell.location.column) if smell.location.column != 0 else ''
        ),
        smell.get_readable_symbol()
    ] for smell in report.code_smells]
    result += get_block(get_table(headers, data))

    # export
    with open(path.join(output_path, 'comment.md'), 'w', encoding='utf-8') as index:
        index.write(result)
