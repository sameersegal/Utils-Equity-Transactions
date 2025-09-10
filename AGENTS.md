# Repository Guidelines

## Project Structure & Module Organization
- `generate_fy_transactions.py`: Main script for processing transactions.
- `transactions.csv`: Source data file (master ledger).
- `pyproject.toml`: Dependency declarations.
- `README.md`: Usage overview.
- `AGENTS.md`: Contributor guide.

## Build, Test, and Development Commands
Install dependencies:
```bash
uv venv --python 3.10
source .venv/bin/activate
uv sync
```
Run the processing script:
```bash
uv run python generate_fy_transactions.py [--owner OWNER ...] [--fy FY18-19]
```
Clean generated files:
```bash
rm FY*.xlsx
```

## Coding Style & Naming Conventions
- Follow PEP 8 for Python code: 4-space indentation, snake_case for functions and variables.
- Use descriptive names (e.g., `start_str`, `financial_years`).
- No tabs. Line length ≤ 88 characters.
- Format code with Black:
```bash
uv run black .
```

## Testing Guidelines
This repository currently has no automated tests. Contributions adding tests should use `pytest` and place tests under `tests/`, naming files `test_*.py`.

## Commit & Pull Request Guidelines
- Write commit messages in imperative mood: “Add feature” not “Added feature”.
- Reference related issues: `Fixes #123`.
- Open PRs against `main` with:
  - A clear description.
  - Linked issue or context.
  - Screenshots or samples if applicable.
- Assign reviewers and wait for approval before merging.

## Security & Configuration Tips
- Do not commit sensitive data (API keys, credentials).
- Treat `transactions.csv` as private financial data.
- Keep `uv.lock` and `requirements.txt` in sync.
