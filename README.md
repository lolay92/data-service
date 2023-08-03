[![test](https://github.com/lolay92/data-service/actions/workflows/ci.yml/badge.svg)](https://github.com/lolay92/data-service/actions/workflows/ci.yml)

# About
This project provides an infrastructure for collecting financial market data from different sources. The project includes a set of loaders for retrieving data from different APIs and a main loader that combines the data from all the sources.

# Project Roadmap
- [x] Poetry for python packages and dependencies management
- [x] Logging configuration
- [x] System implementation for multiple API sources
- [x] Set up a manager for file storage/archivage
- [x] Unitary tests with Pytest
- [x] Makefile
- [x] Workflow automation (CI/CD) with github actions
- [ ] Containerize with Docker
- [ ] Set up a database to store data directly

# Project Structure
The project has the following directory structure:
```bash
.
|-- README.md
|-- output
|-- poetry.lock
|-- pyproject.toml
|-- src
|   `-- data_services
|       |-- __init__.py
|       |-- loader.py
|       |-- loaders
|       |   |-- __init__.py
|       |   |-- api.py
|       |   |-- base.py
|       |   |-- eodhd.py
|       |   `-- tiingo.py
|       `-- utils
|           |-- __init__.py
|           |-- constants
|           |   |-- mykey.ini
|           |   `-- universe.ini
|           |-- fetch_utils.py
|           |-- log_utils.py
|           |-- mykey.py
|           `-- universe.py
`-- tests
    `-- __init__.py
```

<!-- # Installation procedure 
To be completed soon...

# Containerization with Docker
To be completed soon... -->

# License
This project is licensed under the MIT License - see the LICENSE file for details.
