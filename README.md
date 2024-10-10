# larktools


## Development

This package is using [hatch](https://hatch.pypa.io/1.12/) as project managment tool.

Install hatch via `pip`: `pip install hatch`.
For running tests using hatch, see the [hatch run tests documentation](https://hatch.pypa.io/1.9/community/contributing/#run-the-tests).


### Tests

To run the test suite, `pytest` is recommended, and can be done via:

```bash
pytest -v --maxfail=1 larktools/tests/test_suite.py
```

### Debugging

For grammar development using an alternative, less optimized parsing strategy can help avoiding rule conflicts: Use `earley` instead of `lalr`
