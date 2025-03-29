# Contributing to DocRepo

Thank you for considering contributing to DocRepo! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the Issues section
- Use the bug report template when creating a new issue
- Include detailed steps to reproduce the bug
- Describe the expected behavior and what actually happened
- Include system information (OS, Python version, etc.)

### Suggesting Features

- Check if the feature has already been suggested in the Issues section
- Use the feature request template when creating a new issue
- Describe the feature clearly and explain the use case
- Provide examples of how the feature would work

### Contributing Code

#### Setting Up Development Environment

1. Fork the repository
2. Clone your fork locally
3. Set up a virtual environment
4. Install development requirements

```bash
git clone https://github.com/yourusername/docrepo.git
cd docrepo
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

#### Development Workflow

1. Create a new branch for your feature or bug fix
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes
   git checkout -b fix/issue-number-bug-name
   ```

2. Make your changes

3. Ensure your code follows our style guidelines
   - We use [Black](https://black.readthedocs.io/en/stable/) for code formatting
   - We use [isort](https://pycqa.github.io/isort/) for import sorting
   - We use [flake8](https://flake8.pycqa.org/en/latest/) for linting
   
   You can run all checks with:
   ```bash
   # Format code
   black .
   isort .
   
   # Check coding standards
   flake8
   
   # Type checking
   mypy .
   ```

4. Add tests for your changes and ensure all tests pass
   ```bash
   pytest
   ```

5. Update documentation if needed

6. Commit your changes with clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: description of the feature"
   # or
   git commit -m "Fix #123: description of the bug fix"
   ```

7. Push your branch to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a pull request against the main repository

#### Pull Request Guidelines

- Describe what your PR does and why
- Link to related issues if applicable
- Make sure all tests pass
- Keep PRs focused on a single concern
- Update documentation if needed

## Style Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [type hints](https://www.python.org/dev/peps/pep-0484/) for function signatures
- Document code using [docstrings](https://www.python.org/dev/peps/pep-0257/)
- Limit line length to 88 characters (Black default)

### Commit Messages

- Use clear, descriptive commit messages
- Start with an imperative verb (Add, Fix, Update, etc.)
- Reference issues when applicable (Fix #123)

## Testing

- All new features should include tests
- Bug fixes should include a test that prevents regression
- Run the test suite before submitting a PR
- Aim for high test coverage

## Documentation

- Update the README.md if adding new features
- Add or update docstrings for functions and classes
- Update CHANGELOG.md for significant changes

## License

By contributing to DocRepo, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 