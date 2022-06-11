"""
The command line module provides the main function of the application.
"""
# from asyncio import subprocess
import subprocess
import sys
import json
import re
from pathlib import Path
from os import path, getcwd
import click
from smelly_python.code_smell import Report
from smelly_python.generator.pylint_explanation_fetcher import ExplanationFetcher
from smelly_python.generator.webpage_generator import generate_webpage
from smelly_python.generator.md_generator import generate_md


def get_grade(text: str) -> str:
    """
    Extracts the grade from the text exported by pylint.
    :param: text the exported text
    :return: the grade with one decimal place
    """
    search = re.search(r'Your code has been rated at (\d+)\.?(\d*)', text)

    if search.group(2).lstrip('0') == '':
        return search.group(1)

    return search.group(1) + '.' + search.group(2)


@click.command()
@click.option('--directory', '-d', type=click.Path(exists=True),
              help='Specify the python main directory for pylint.')
def main(directory):
    """
    Main command line interface.
    Takes the first command line argument to be the directory that pylint should analyse.
    """
    if not directory:
        print("Please provide the --dir parameter")
        sys.exit(1)
    _setup_dirs()
    print('Running pylint...')
    result = None
    try:
        result = subprocess.run(['pylint', directory, f'--output-format=json:'
        f'{_get_reports("report.json")},text:{_get_reports("grade.txt")}', '--exit-zero'],
                                capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        print(
            f'Whoops we could not run pylint for the following directory: {directory}')
        print(result.stderr)
        sys.exit(1)
    print('Finished running python, creating report...')
    with open(_get_reports('report.json'), 'r', encoding='utf-8') as input_file:
        content = json.load(input_file)
    with open(_get_reports('grade.txt'), 'r', encoding='utf-8') as input_file:
        grade = get_grade(input_file.read())

    report = Report(content, grade)
    explanations = ExplanationFetcher()
    generate_webpage(report, explanations)
    generate_md(report, explanations)

    print('Success!')


def _setup_dirs():
    Path(path.join('report', 'smelly_python')).mkdir(parents=True, exist_ok=True)


def _get_reports(file_name):
    return path.join(getcwd(), 'report', 'smelly_python', file_name)


if __name__ == '__main__':
    main(None)
