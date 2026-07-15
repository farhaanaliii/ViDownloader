# Contributing to ViDownloader

Thank you for considering contributing to ViDownloader! This document outlines the process for contributing to make it as smooth as possible.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (links, screenshots, error messages)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (OS, Python version, PyQt5 version)

### Suggesting Features

Feature suggestions are welcome! Please:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested feature
- **Explain why this feature would be useful** to most users
- **List any alternative solutions** you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the existing code style** (see Style Guide below)
3. **Write clear, descriptive commit messages**
4. **Test your changes** thoroughly
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description of changes

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/farhaanaliii/vidownloader.git
cd vidownloader
```

2. Install in editable mode with all dev dependencies:
```bash
pip install -e ".[dev]"
```

This installs all development dependencies automatically: `pytest`, `pytest-qt`, `pytest-cov`, `pytest-mock`, `black`, `isort`, `flake8`, and `pyinstaller`.

4. Run tests:
```bash
pytest
```

## Code Style Guide

ViDownloader follows these conventions:

### Python Code

- **PEP 8** compliance (with some flexibility for readability)
- **Type hints** where applicable
- **Docstrings** for classes and complex functions
- **Meaningful variable names** (avoid single letters except for loops)

### Project Structure

```
vidownloader/
├── core/           # Core functionality (models, utilities, workers)
├── ui/             # UI components (layouts, stylesheets, dialogs)
├── window/         # Main windows (HomeWindow, MainWindow)
└── main.py         # Entry point
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `MainWindow`, `VideoDownloader`)
- **Functions/Methods**: `snake_case` (e.g., `download_video`, `parse_url`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_THREADS`, `API_KEY`)
- **Private methods**: Prefix with `_` (e.g., `_internal_helper`)

### Method Prefixes

- `init_*` - Initialization methods
- `action_*` - User action handlers
- `signal_*` - Signal/slot handlers (use `@pyqtSlot` decorator)

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add playlist scraping support
Fix download progress bar not updating
Update README with installation instructions
Refactor Scraper class for better performance
```

## Testing

- Write tests for new features
- Ensure existing tests pass before submitting PR
- Test on your local environment (Windows/Linux)
- Include both unit tests and integration tests where appropriate

## Documentation

- Update README.md if you change functionality
- Add docstrings to new classes/methods
- Update changelog in `dialogs.py` for user-facing changes
- Keep comments clear and concise

## What to Expect

- **Response time**: We'll try to respond to issues/PRs within 2-3 days
- **Feedback**: Constructive feedback may be provided on PRs
- **Iteration**: Be prepared to make changes based on review
- **Appreciation**: All contributions are valued, even small fixes!

## Questions?

If you have questions, feel free to:
- Open an issue with the "question" label
- Reach out to [@farhaanaliii](https://github.com/farhaanaliii)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make ViDownloader better!**
