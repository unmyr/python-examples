.PHONY: test coverage

test:
	python -m unittest discover --start-directory tests -v --pattern 'test_*.py'

coverage:
	coverage run --source src/dict -m unittest discover -s tests
	coverage report -m
	coverage xml