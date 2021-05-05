echo "Reformating..."
black main.py src/ tests/

echo "Running Type Hint checks"
mypy src/ tests/

echo "Running tests"
pytest tests/

echo "Running Lint checks"
pylint src tests/

echo "Checked performed"
