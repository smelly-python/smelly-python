"""
The md generator module provides the method that generates the md comment given a list of
style errors.
"""
from os import path

from smelly_python.code_smell import Report
from smelly_python.generator.pylint_explanation_fetcher import ExplanationFetcher


def get_block(string):
    """
    Gets a string as an MD block.
    :param: string the string to format
    :return: the string as an MD block
    """
    return f'{string}\n\n'


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
    table += f'| {" | ".join(headers)} |\n'
    # line
    table += f'|{"|".join(["-" * (len(header) + 2) for header in headers])}|\n'
    # data
    for smell in data:
        table += f'| {" | ".join(smell)} |\n'

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


def generate_md(report: Report, explanations: ExplanationFetcher,
                output_path: str = path.join('report', 'smelly_python')):
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
        + get_code_smell_number_string(len(report.code_smells))
        + ' in your project.'
    )

    if report.is_clean():
        # congratulations
        result += get_block('Good job! :partying_face:')

    else:
        result +=\
            get_block('You can find the more detailed html report in the artifact of the action.')
        result +=\
            get_block('On a PR, the artifact can be found at the right top of the `Checks` tab.')
        # table
        headers = ['', 'File', 'Lines', 'Smell', 'Explanation']
        data = [[
            smell.type.value,
            f'`{smell.location.path}`',
            '`' + str(smell.location.line) + (
                ':' + str(smell.location.column) if smell.location.column != 0 else ''
            ) + '`',
            smell.get_readable_symbol(),
            explanations.get_explanation(smell.message_id).to_markdown()
        ] for smell in report.code_smells]
        result += get_block(get_table(headers, data))

    # export
    with open(path.join(output_path, 'comment.md'), 'w', encoding='utf-8') as index:
        index.write(result)
