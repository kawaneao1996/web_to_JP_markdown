# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Setup: `pip install -r requirements.txt`
- Run CLI app: `python main.py -i "URL" -o "./output.md"`
- Run Web app: `streamlit run app.py`

## Code Style Guidelines

- **Python**: Follow PEP 8 style guide
- **Imports**: Group imports by standard library, third-party, and local
- **Formatting**: Use 4 spaces for indentation
- **Types**: Use type hints for function parameters and return values
- **Naming**:
  - snake_case for variables and functions
  - CamelCase for classes
- **Error Handling**: Use try/except blocks for web requests and file operations
- **Documentation**: Docstrings for functions and classes, inline comments for complex logic
- **Language**: Code comments and documentation in Japanese, variable names in English
