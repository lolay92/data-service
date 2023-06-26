lint: 
	flake8 src/data_services/

format: 
	black src/data_services/

all: lint format
