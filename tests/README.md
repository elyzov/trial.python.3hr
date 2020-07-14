# tests directory

This directory contains all the automated tests for the test tool `py.test`.

**`.coverage`**: Configuration file for the Python coverage tool `coverage`.

**`conftest.py`**: Defines fixtures for py.test.

**`test_*`**: py.test will load any file that starts with the name `test_`
and run any function that starts with the name `test_`.


## Testing the app

    # Run all the automated tests in the tests/ directory
    py.test -s tests/
