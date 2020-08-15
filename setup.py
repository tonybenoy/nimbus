from setuptools import (
    find_packages,
    setup,
)

DEV_REQUIRES = [
    "black",
    "pylint",
    "pre-commit",
    "mypy",
    "sqlalchemy-stubs",
    "pytest",
    "pytest-cov",
    "mkdocs",
]

setup(
    name="nimbus",
    version="0.1",
    author="Tony Benoy",
    author_email="me@tonybenoy.com",
    license="MIT",
    description="Setup for Nimbus Backend",
    python_requires=">=3.8",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "alembic",
        "psycopg2-binary",
        "sqlalchemy",
        "parse",
        "pytest",
        "pydantic",
        "docker",
        "pytest-mypy",
        "pytest-black",
        "pytest-isort",
        "isort",
        "pendulum",
        "pytest-cov",
        "fastapi",
        "gunicorn",
        "starlette",
        "httpx",
    ],
    extras_require={"dev": DEV_REQUIRES},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3.8",],
)
