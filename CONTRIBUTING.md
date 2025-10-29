# Contributing to CIV-ARCOS

**Civilian Assurance-based Risk Computation and Orchestration System**

*"Military-grade assurance for civilian code"*

Thank you for your interest in contributing to CIV-ARCOS! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/J-Ellette/CIV-ARCOS.git
   cd CIV-ARCOS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

## Code Standards

### Style Guide

We use the following tools to maintain code quality:

- **Black** for code formatting
- **MyPy** for type checking
- **Flake8** for linting

Run these tools before submitting:

```bash
# Format code
black civ_arcos/ tests/

# Type check
mypy civ_arcos/

# Lint
flake8 civ_arcos/ tests/
```

### Testing

All code changes should include tests:

- Unit tests go in `tests/unit/`
- Integration tests go in `tests/integration/`
- Aim for >80% test coverage
- All tests must pass before submitting

Run tests with coverage:

```bash
pytest --cov=civ_arcos --cov-report=html
```

## Project Philosophy

### What We Don't Use

CIV-ARCOS is built from scratch without the following frameworks:
- Django, FastAPI, Flask (we emulate them)
- Django ORM, SQLAlchemy, Peewee/Tortoise (we build our own)
- Django-allauth, Authlib, PassLib (we create our own)
- Django Templates, Jinja2 (we build our own)
- Django REST Framework, Pydantic (we emulate them)
- Redis-py, Django Cache Framework (we create alternatives)

### What We Can Use

We allow these tools where needed:
- pytest, Coverage.py
- Black, MyPy, Flake8
- Docker

### Why?

We're building a complete system from fundamental principles to:
1. Understand every component deeply
2. Minimize external dependencies
3. Create a military-grade assurance foundation
4. Maintain full control over security and integrity

## Development Workflow

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following our style guide
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes:**
   ```bash
   pytest
   black civ_arcos/ tests/
   mypy civ_arcos/
   flake8 civ_arcos/ tests/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Areas for Contribution

### High Priority

- **Step 2: Automated Test Evidence Generation**
  - Static analysis modules
  - Dynamic testing integration
  - Coverage analysis tools
  - Security scanning integration

- **Step 3: Digital Assurance Case Builder**
  - Argument template system
  - Evidence linking
  - GSN notation support

- **Additional Adapters**
  - PyTest adapter
  - Jest adapter
  - SonarQube adapter
  - Coverage.py integration

### Medium Priority

- Web dashboard UI
- More badge types
- Documentation improvements
- Example projects
- Integration tests

### Low Priority

- Performance optimizations
- Additional storage backends
- CLI improvements

## Code Review Process

All submissions require review:

1. Code must follow style guidelines
2. Tests must pass and coverage must be maintained
3. Documentation must be updated
4. Changes must align with project philosophy

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in existing issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.
