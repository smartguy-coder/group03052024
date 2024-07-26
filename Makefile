.PHONY: run
run:
	echo '1111'
	@echo '22222'
	uvicorn main:app --reload --port 8001


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


.PHONY: pot
pot:
	xgettext -i web_router/web.py -o transl.pot -d this_project;

.PHONY: lang-structure
lang-structure:
	@echo 'Starting lang-structure...'
	mkdir -p locale/en/LC_MESSAGES
	mkdir -p locale/it/LC_MESSAGES
	@echo 'lang-structure finished'

.PHONY: lang-po
lang-po:
	msginit -i transl.pot -o locale/uk/LC_MESSAGES/this_project.po -l uk
	msginit -i transl.pot -o locale/ru/LC_MESSAGES/this_project.po -l ru
	msginit -i transl.pot -o locale/it/LC_MESSAGES/this_project.po -l it
	msginit -i transl.pot -o locale/en/LC_MESSAGES/this_project.po -l en

.PHONY: lang-mo
lang-mo:
	msgfmt  locale/uk/LC_MESSAGES/this_project.po -o locale/uk/LC_MESSAGES/this_project.mo
	msgfmt  locale/ru/LC_MESSAGES/this_project.po -o locale/ru/LC_MESSAGES/this_project.mo
	msgfmt  locale/it/LC_MESSAGES/this_project.po -o locale/it/LC_MESSAGES/this_project.mo
	msgfmt  locale/en/LC_MESSAGES/this_project.po -o locale/en/LC_MESSAGES/this_project.mo

.PHONY: merge-po
merge-po:
	msgmerge --update locale/en/LC_MESSAGES/this_project.po transl.pot
	msgmerge --update locale/uk/LC_MESSAGES/this_project.po transl.pot
	msgmerge --update locale/ru/LC_MESSAGES/this_project.po transl.pot
	msgmerge --update locale/it/LC_MESSAGES/this_project.po transl.pot
