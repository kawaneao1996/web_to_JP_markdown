# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Setup**: `pip install -r requirements.txt`
- **Run CLI app**: `python main.py -i "URL" -o "./output.md"`
- **Run Web app**: `streamlit run app.py`
- **Run MCP server**: `python mcp_server.py`
- **Lint and format**: `ruff check` and `ruff format`

## Architecture Overview

### Core Components

- **`WebToMarkdownTranslator` class** (`main.py`): Main engine that handles the entire translation pipeline:
  - Web content fetching with user-agent headers
  - HTML parsing and main content extraction using selectors (article, main, etc.)
  - HTML-to-markdown conversion with markdownify
  - Japanese translation using Google Gemini 2.0 Flash model

### Application Interfaces

- **CLI app** (`main.py`): Command-line interface for single URL processing
- **Web app** (`app.py`): Streamlit-based GUI with real-time preview and download functionality
- **MCP server** (`mcp_server.py`): FastMCP server exposing translation tools for external integration

### Configuration

- **Environment variables**: `GEMINI_API_KEY` required for translation functionality
- **Ruff configuration** in `pyproject.toml`: Line length 79, double quotes, 4-space indentation
- **Dependencies**: Google GenAI, BeautifulSoup4, markdownify, Streamlit, MCP

## Translation Pipeline

1. **Fetch**: HTTP request with proper headers to retrieve HTML content
2. **Extract**: Parse HTML and identify main content using semantic selectors
3. **Convert**: Transform HTML to markdown using markdownify with ATX headers
4. **Translate**: Send to Gemini API with specific prompt for Japanese translation while preserving markdown formatting

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
