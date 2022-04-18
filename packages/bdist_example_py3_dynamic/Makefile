TARGET_BDIST=dist/example_package_py3-0.0.1-py3-none-any.whl
TARGET_SDIST=dist/example-package-py3-0.0.1.tar.gz
PACKAGE_NAME=example-package-py3
TARGETS=\
$(TARGET_BDIST) \
$(TARGET_SDIST)

.PHONY: build

build: $(TARGETS)

$(TARGET_BDIST):
	python3 setup.py sdist bdist_wheel

$(TARGET_SDIST):
	python3 setup.py sdist bdist_wheel

install: $(TARGET_BDIST)
	python3 -m pip install $<

uninstall:
	python3 -m pip uninstall -y $(PACKAGE_NAME)

clean:
	rm -f $(TARGETS)
