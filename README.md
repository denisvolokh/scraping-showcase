# Data Theorem Assessment

## Setup Dev Environment

### Checkout the code

```bash
git clone git@github.com:denisvolokh/data-theorem-assessment.git
```

### Install Poetry and packages

```bash
pip install poetry
poetry install
```

### Activate the virtual environment

```bash
poetry shell
```

### Install pre-commit hooks

```bash
poetry run pre-commit install
```

Note: if it fails with the error `FatalError: git failed` need to initialize git repository first:

```bash
git init
```

### Run application in Docker Compose

```bash
docker-compose up -d
```

Verify that all services are running:

```bash
docker-compose ps
```

Expected output:

```bash
Name    | Image                           | Created         | Status     |    Ports               |
--------|---------------------------------|-----------------|------------|------------------------|
api     | data-theorem-assessment-api     | 2 minutes ago   | Up         | 0.0.0.0:5000->5000/tcp |
mkdocs  | data-theorem-assessment-mkdocs  | 2 minutes ago   | Up         | 0.0.0.0:5002->5002/tcp |
redis   | redis:latest                    | 2 minutes ago   | Up         | 0.0.0.0:6379->6379/tcp |
tasks   | data-theorem-assessment-tasks   | 2 minutes ago   | Up         |                        |
webapp  | data-theorem-assessment-webapp  | 2 minutes ago   | Up         | 0.0.0.0:5001->5001/tcp |
```

The API server is available at [http://0.0.0.0:5000/](http://0.0.0.0:5000/).

The MkDocs server is available at [http://0.0.0.0:5002/](http://0.0.0.0:5002/).

The web application is available at [http://0.0.0.0:5001/](http://0.0.0.0:5001/).


## Code Quality

The project is configured to use [pre-commit](https://pre-commit.com/) hooks to run tools isort, black, flake8, and mypy to ensure code quality. The following hooks are configured:

- [isort](https://pypi.org/project/isort/) - sorts imports
- [black](https://pypi.org/project/black/) - formats code
- [flake8](https://flake8.pycqa.org/en/latest/) - lints code
- [mypy](https://mypy.readthedocs.io/en/stable/) - type checks code

The pre-commit configuration is stored in the `.pre-commit-config.yaml` file and hooks are configured in the `pyproject.toml` file.

The hooks are configured to run automatically on commit but can also be run manually. To run the hooks manually, run the following command:

```bash
poetry run mypy
```

## Testing

The project is configured to use [pytest](https://docs.pytest.org/en/stable/) to run tests. The tests are stored in the `api/tests` To run the tests manually, run the following command:

```bash
pytest
```

Note: Make sure that pytest executable is installed in the virtual environment. To check which pytest executable is used, run the following command:

```bash
which pytest
```

It should return the path to the pytest executable in the virtual environment:

```bash
/Users/denys.volokh/Library/Caches/pypoetry/virtualenvs/data-theorem-assessment-oHUsPNxH-py3.10/bin/pytest
```