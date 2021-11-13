# Contributing to Static Site Generator

Welcome to the Contribution Page!  This page provides useful information about contributing to the tool

## Contribution Process
The contribution process starts with filing an issue on GitHub issue page. We define 4 categories of issues:
- Feature Request
- Bug Reports
- Documentation
- Installation Issues

Once you filed an issue, you may begin working on implementing a feature or fixing a bug. Lastly, create your Pull Request with an explanation of changes you have made. One of the members of the tool will review your Pull Request.

Congratulations, you have contributed to the Tool!

## Contribution Guidelines
In this section, we provide guidelines to consider as you develop new features or bug fixes.

### Installing dependencies
Before you begin working with tool, you need to install required dependencies.
```
pip3 install -r requirements.txt
```
If you plan on doing development and testing, you will also need to install the dependencies dedicated for testing.
```
pip3 install -r dev-requirements.txt
```
### Developing and Testing the Tool

Once you develop a new feature or fix a bug, we recommend running a code formatter. We use [Black](https://black.readthedocs.io/en/stable/) to ensure a consistent code format. You can run auto-format your code by running:
```
black .
```
Then, verify that linter pass before submitting a Pull Request by running:
```
flake8 .
```
Verify that unit tests pass before submitting a Pull Request by running:
```
pytest tests/
```