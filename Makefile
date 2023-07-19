.ONESHELL: 

lint: 
	flake8 src/data_services/
	flake8 tests/

format: 
	black src/data_services/
	black tests/

run_unit_tests: 
	@echo "Running a battery of tests..."
	pytest -s -q --disable-pytest-warnings tests/unit/loaders/test_eodhd.py
	pytest -s -q --disable-pytest-warnings tests/unit/test_loader.py
	pytest -s -q --disable-pytest-warnings tests/unit/utils/test_fetch_utils.py
	@echo "Tests carried out successfully!"

all: lint format run_unit_tests

.PHONY:  lint format run_unit_tests 