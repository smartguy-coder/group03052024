.PHONY: run
run:
	echo '1111'
	@echo '22222'
	python main.py

#.PHONY: ins
#ins:
#	pip install poetry
#	poetry config --local virtualenvs.in-project true
#	poetry init -n
#	poetry install
#	.\.venv\Scripts\activate
#	poetry add fastapi

.PHONY: c
c:
	@echo 'Starting code correction...'
	black .
	isort .
	flake8 .
	pytest .
	@echo 'FINISH'
