# About
This project provides an infrastructure for collecting financial market data from different sources. The project includes a set of loaders for retrieving data from different APIs and a main loader that combines the data from all the sources.

# Project Roadmap
- [x] Poetry for python packages and dependencies management
- [x] Logging configuration
- [x] System implementation for multiple API sources
- [ ] Set up a manager for file storage/archivage
- [ ] Containerize with Docker
- [ ] Unitary tests with Pytest
- [ ] Makefile
- [ ] Workflow automation (CI/CD) with github actions

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
- **'output'** directory stores the output files
- **'poetry.lock'** and **'pyproject.toml'** files contain project dependencies and configuration details
- **'src'** directory contains the source code for the project
- **'data_services'** module contains the loaders and main loader code
- **'loaders'** sub-module contains different data loaders for different APIs
- **'utils'** sub-module contains utility functions and constants
- **'tests'** directory contains test code for the project

<!-- # Installation procedure 
To be completed soon...

# Containerization with Docker
To be completed soon... -->

# License
This project is licensed under the MIT License - see the LICENSE file for details.
