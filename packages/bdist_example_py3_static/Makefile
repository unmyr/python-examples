TARGET_BDIST=dist/example_package_py3-0.0.1-py3-none-any.whl
TARGET_SDIST=dist/example-package-py3-0.0.1.tar.gz
PACKAGE_NAME=example-package-py3
TARGETS=\
$(TARGET_BDIST) \
$(TARGET_SDIST)

SOURCES=\
setup.cfg \
src/example_package/__init__.py \
src/example_package/calc.py

.PHONY: build

build: $(TARGETS)

upgrade:
	python3 -m pip install --upgrade build

$(TARGET_BDIST): $(SOURCES)
	python3 -m build

install: $(TARGET_BDIST)
	python3 -m pip install --find-links dist $(PACKAGE_NAME)

uninstall:
	python3 -m pip uninstall -y $(PACKAGE_NAME)

show:
	python3 -m pip show example-package-py3
	python3 -m pip show -f example-package-py3

test_installed:
	python -m unittest discover -s src tests/

test_local:
	PYTHONPATH=src python -m unittest discover -s src tests/

clean:
	rm -fR dist/ build/ src/*.egg-info
