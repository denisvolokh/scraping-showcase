# Setup

## Dev Environment

### Checkout the code

```bash
git clone git@github.com:denisvolokh/data-theorem-assessment.git
```

### Install Poetry and packages

```bash
pip install poetry
poetry install
```

### Install pre-commit hooks

```bash
poetry run pre-commit install
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

## Testing

### Enter the container

```bash
docker exec -it api bash
```

### Run tests

```bash
pytest
```