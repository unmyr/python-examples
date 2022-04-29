TARGET_BDIST=dist/example_package-0.0.1-py3-none-any.whl
TARGET_SDIST=dist/example-package-0.0.1.tar.gz
PACKAGE_NAME=example-package
TARGETS=\
$(TARGET_BDIST) \
$(TARGET_SDIST)

.PHONY: build bdist sdist

build: $(TARGETS)

$(TARGET_BDIST):
	python3 setup.py sdist bdist_wheel

$(TARGET_SDIST):
	python3 setup.py sdist

bdist: $(TARGET_BDIST)
	python3 setup.py bdist_wheel

sdist: $(TARGET_SDIST)
	python3 setup.py sdist

install_bdist: $(TARGET_BDIST)
	python3 -m pip install --no-index --find-links dist $(PACKAGE_NAME)

install_sdist: $(TARGET_SDIST)
	python3 -m pip install $^

show:
	python3 -m pip show $(PACKAGE_NAME)
	python3 -m pip show -f $(PACKAGE_NAME)

test_installed:
	python -m unittest discover -s src tests/

test_local:
	PYTHONPATH=. python -m unittest discover -s src tests/

uninstall:
	python3 -m pip uninstall -y $(PACKAGE_NAME)

clean:
	rm -fR dist/ build/ src/*.egg-info
