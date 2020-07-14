.PHONY: build
build:
	python setup.py sdist bdist_wheel


.PHONY: test
test:
	pipenv run flake8 pymonads --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy pymonads
	pytest