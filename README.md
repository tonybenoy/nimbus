<p>
    <a href="https://github.com/tonybenoy/nimbus/actions">
        <img src="https://github.com/tonybenoy/nimbus/workflows/Tests/badge.svg" alt="Test Status" height="18">
    </a>
    <a href="https://github.com/tonybenoy/nimbus/actions">
        <img src="https://github.com/tonybenoy/nimbus/workflows/pre-commit%20hooks/badge.svg" alt="Pre-commit Status" height="18">
    </a>
</p>
<p>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python version" height="18"></a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Codestyle Black" height="18">
    </a>
</p>

### Setup

- make sure you are using python > 3.8+
- setup virtualenv using`virtualenv env` and activate it
- run`pip install -e .` to install dependencies and setup new added dependencies
- run`black . && isort . && pytest --mypy --black --isort --cov=nimbus --cov-report=xml --cov-report=term` to run your tests
- all source code is under`src/nimbus/`.


# To run server on docker file
`docker build -t nimbus   .`
`docker run -it -p 4000:4000 nimbus`
