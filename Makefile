PWD = $(shell pwd)

check:
	flake8
	ruff check --ignore E501 .
	pytest

clean:
	rm -rf $(PWD)/build $(PWD)/dist $(PWD)/pysafebrowsing.egg-info

dist:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

test:
	pytest
