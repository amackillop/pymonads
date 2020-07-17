TAG ?= $(tag)

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: release
release:
ifeq ($(TAG),)
	echo "Please provide a release tag"
else
	twine upload dist/pymonads-$(TAG)*
endif


.PHONY: test
test:
	pipenv run flake8 pymonads --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy pymonads
	pytest