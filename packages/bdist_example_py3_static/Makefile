TARGET_BDIST=dist/example_package_py3-0.0.1-py3-none-any.whl
TARGET_SDIST=dist/example-package-py3-0.0.1.tar.gz
PACKAGE_NAME=example-package-py3
TARGETS=\
$(TARGET_BDIST) \
$(TARGET_SDIST)

.PHONY: build

build: $(TARGETS)

upgrade:
	python3 -m pip install --upgrade build

$(TARGET_BDIST):
	python3 -m build

install: $(TARGET_BDIST)
	python3 -m pip install $<

uninstall:
	python3 -m pip uninstall -y $(PACKAGE_NAME)

clean:
	rm -f $(TARGETS)
