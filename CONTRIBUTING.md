# Contributing to Customer Churn Prediction Project

Thank you for your interest in contributing!

## How to Contribute

### Reporting Issues
- Search existing issues before creating a new one
- Use issue templates when available
- Include dataset version and steps to reproduce

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Include type hints where applicable
- Write unit tests for new features

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Reference issues when applicable

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Customer-Churn-Prediction-Retention-Strategy.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Project Structure

```
churn_prediction/
├── src/                    # Source code
├── tests/                  # Test files
├── data/                   # Data files
├── results/               # Output results
└── docs/                  # Documentation
```

## Questions?
Open an issue or reach out to the maintainers.
