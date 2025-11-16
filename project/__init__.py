"""Invoke task modules for project automation.

This package contains modular task definitions for various development tools including:
- Code quality checks (ruff, mypy)
- Testing (pytest, tox)
- Security scanning (pip-audit, pre-commit)
- Code analysis (vulture, xenon, deptry)
- Project-level orchestration tasks

Each module exports a 'collection' object that is registered in the root tasks.py file.
"""
