# Smelly Python

A python code smell reporting tool, created for the course Release [Engineering for Machine Learning applications](https://se.ewi.tudelft.nl/remla/2022/).

The tool generates a html report for easy viewing of pylint errors.

# How to use
1. Run `pip install smelly-python` 
2. Run `smelly-python -d {src}`. Replace `src` with the directory which should be analysed. 
3. Open `./report/smelly_python/index.html` to view the generated report. 

# Using more advanced features
smelly-python will run the following command: `pylint {src} --output-format:json:report.json,text:grade.txt --exit-zero` where `src` it the previously mentioned input directory from the command.

In order to further customize the running of pylint, use the `.pylintrc` file to configure pylint. 

# Using in github actions
The tool has been designed to be run in a github action using [smelly-my-pr](https://github.com/marketplace/actions/smelly-python-smell-my-pr). The action will automatically post the output of the tool to your github pull requests and add a summary to the job. 