# 0x03. Unittests and Integration Tests

This project covers the difference between **unit tests** and **integration tests**, and introduces common testing patterns such as **mocking**, **parameterization**, and **fixtures**.

## Learning Objectives
- Understand the difference between unit and integration tests
- Use the `unittest` framework in Python
- Write parameterized tests with `parameterized.expand`
- Mock external dependencies during unit tests
- Structure test files for Python projects

## Files
- `utils.py` – helper functions (access_nested_map, get_json, memoize)
- `client.py` – GithubOrgClient class for working with GitHub orgs
- `fixtures.py` – sample payloads for testing
- `test_utils.py` – unit tests for utils.py

## Running Tests
From the project directory:

```bash
python -m unittest test_utils.py
