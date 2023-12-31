# DangerDine

"It will boost your immune system!"

An exciting web app that suggests restaurants to eat at in your local area that have a very poor food hygiene rating

[![Tests](https://github.com/CarrotManMatt/DangerDine/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/CarrotManMatt/DangerDine/actions/workflows/tests.yaml)

## Installing

DangerDine uses Python 3.11, please ensure you have this version installed (downloads available [here](https://www.python.org/downloads/release/python-3116/#Files))

### Geospatial Database

For windows install using these 3 links (in order):
* http://www.gaia-gis.it/gaia-sins/windows-bin-x86
* https://trac.osgeo.org/osgeo4w/ (Select Express Web-GIS Install and click next. In the ‘Select Packages’ list, ensure that GDAL is selected. If any other packages are enabled by default, they are not required by GeoDjango and may be unchecked safely)
* https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/#modify-windows-environment

For linux install using this command:

```shell
sudo apt install libsqlite3-mod-spatialite && sudo apt install binutils libproj-dev gdal-bin
```

### Dependencies

Ensure that you have [Poetry](https://python-poetry.org/) installed (instructions can be found [here](https://python-poetry.org/docs/#installation)), then navigate to the root folder and run the following command:

```shell
poetry install --no-root && poetry run pre-commit install
```

Poetry will complain if you do not have the correct Python version installed. Follow the steps in [Installing](#Installing) to get the correct version

## Environment Variables

To run the program you may need to set some environment variables (E.g. `SECRET_KEY`), the required ones are specified in `.example.env` and must be placed into a file called `.env` in the project root.

## Contributions

Contributions are welcome. If you want to contribute, please raise a PR, and we'll review, test and (likely) merge it. Please comment on issues you'd like to work on for assignment to prevent duplication of work. If you find any bugs/problems or have any feature suggestion, please raise an issue.

Please ensure your new code adheres to [mypy](https://www.mypy-lang.org/)'s type checking & [ruff](https://ruff.rs/)'s linting so that the repo has a consistent style. By also running [pytest]()'s test suite you can ensure your contributions provide valid functionality.