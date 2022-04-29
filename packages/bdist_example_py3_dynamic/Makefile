TARGET_BDIST=dist/example_package_py3-0.0.1-py3-none-any.whl
TARGET_SDIST=dist/example-package-py3-0.0.1.tar.gz
PACKAGE_NAME=example-package-py3
TARGETS=\
$(TARGET_BDIST) \
$(TARGET_SDIST)

SOURCES=\
setup.py \
src/example_package/__init__.py \
src/example_package/calc.py

.PHONY: build build_sdist build_bdist install_bdist install_sdist

build: $(SOURCES)
	python3 setup.py sdist bdist_wheel

$(TARGET_BDIST): $(SOURCES)
	python3 setup.py bdist_wheel

$(TARGET_SDIST): $(SOURCES)
	python3 setup.py sdist

build_sdist: $(TARGET_SDIST)

build_bdist: $(TARGET_BDIST)

install_bdist: $(TARGET_BDIST)
	python3 -m pip install --find-links dist $(PACKAGE_NAME)

install_sdist: $(TARGET_SDIST)
	python3 -m pip install $<

uninstall:
	python3 -m pip uninstall -y $(PACKAGE_NAME)

show:
	python3 -m pip show $(PACKAGE_NAME)
	python3 -m pip show -f $(PACKAGE_NAME)

test_installed:
	python -m unittest discover -s src tests/

test_local:
	PYTHONPATH=src python -m unittest discover -s src tests/

clean:
	rm -fR dist/ build/ src/*.egg-info
