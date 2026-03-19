.PHONY: help install test clean run lint format docs

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run the complete pipeline"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean generated files"
	@echo "  make docs       - Build documentation"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run:
	python main.py

lint:
	flake8 src/ --max-line-length=100 --ignore=E501,W503
	mypy src/ --ignore-missing-imports

format:
	black src/ --line-length=100
	isort src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/
	rm -rf results/models/*.pkl results/*.db

docs:
	sphinx-build -b html docs/ docs/_build/

eda:
	python -c "from src.eda_analysis import ChurnEDA; import pandas as pd; eda = ChurnEDA(pd.read_csv('data/customer_data.csv')); eda.generate_eda_report()"

insights:
	python -c "from src.insights_recommendations import ChurnInsights; import pandas as pd; insights = ChurnInsights(pd.read_csv('data/customer_data.csv')); insights.generate_full_report()"
