# Smelly Python

A code smell reporting tool for Python projects, created for the [Release Engineering for Machine Learning applications](https://se.ewi.tudelft.nl/remla/2022/) course at TU Delft.

Smelly Python generates an HTML report for easy viewing of Pylint errors.

# How To
1. Run `pip install smelly-python` 
2. Run `smelly-python -d {src}`. Replace `{src}` with the directory you want to analyse.
3. Open `./report/smelly_python/index.html` to view the generated report. 

# Using Advanced Features of Pylint
Smelly Python will run the following command: `pylint {src} --output-format:json:report.json,text:grade.txt --exit-zero`. Therefore, in order to customize what settings Pylint runs with, use the `.pylintrc` file to configure it. 

# Using Smelly-Python in GitHub Actions
The tool has been designed to be run within a GitHub workflow using the [smell-my-pr](https://github.com/marketplace/actions/smelly-python-smell-my-pr) GitHub action. The action will automatically post the output of the tool to your GitHub pull request as a comment and add a summary and artifact to the job. 