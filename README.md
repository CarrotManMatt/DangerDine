# DangerDine

"It will boost your immune system!"

An exciting web app that suggests restaurants to eat at in your local area that have a very poor food hygiene rating

[![Tests](https://github.com/CarrotManMatt/DangerDine/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/CarrotManMatt/DangerDine/actions/workflows/tests.yaml)

## Installing

DangerDine uses Python 3.11, please ensure you have this version installed (downloads available [here](https://www.python.org/downloads/release/python-3116/#Files))

### Dependencies

Ensure that you have [Poetry](https://python-poetry.org/) installed (instructions can be found [here](https://python-poetry.org/docs/#installation)), then navigate to the root folder and run the following command:

```shell
poetry install --no-root
```

Poetry will complain if you do not have the correct Python version installed. Follow the steps in [Installing](#Installing) to get the correct version

## Contributions

Contributions are welcome. If you want to contribute, please raise a PR, and we'll review, test and (likely) merge it. Please comment on issues you'd like to work on for assignment to prevent duplication of work. If you find any bugs/problems or have any feature suggestion, please raise an issue.

Please ensure your new code adheres to [mypy](https://www.mypy-lang.org/)'s type checking & [ruff](https://ruff.rs/)'s linting so that the repo has a consistent style. By also running [pytest]()'s test suite you can ensure your contributions provide valid functionality.