BASE_DIR=..
DOC_ROOT=.

DEST_DIR=$(BASE_DIR)/dist
SRC_IMAGES_DIR=$(IMAGES_DIR)
DST_IMAGES_DIR=$(DEST_DIR)/$(IMAGES_DIR)

include $(DOC_ROOT)/asciidoc.mk

HTML_LIST=\
mkdir_and_copy \
$(DEST_DIR)/install_pyenv.html \
$(DEST_DIR)/linter.html \
$(DEST_DIR)/matplotlib/index.html \
$(DEST_DIR)/sqlalchemy.html \
$(DEST_DIR)/string.html \
$(DEST_DIR)/sympy/index.html \
$(DEST_DIR)/index.html

.PHONY: adoc mkdir_and_copy

adoc: $(HTML_LIST)

mkdir_and_copy:
	mkdir -p $(DEST_DIR)
	-test ! -d $(SRC_IMAGES_DIR) || mkdir -p $(DST_IMAGES_DIR)
	-test ! -d $(SRC_IMAGES_DIR) || cp $(CP_OPTS) $(SRC_IMAGES_DIR)/* $(DST_IMAGES_DIR)/

$(DEST_DIR)/%.html: %.adoc header.adoc
	asciidoctor --trace $(AD_OPTS_HTML5_ROUGE) -o "$@" "$<"

$(DEST_DIR)/matplotlib/index.html: matplotlib/index.adoc
	(cd matplotlib && make adoc)

$(DEST_DIR)/sympy/index.html: sympy/index.adoc
	(cd sympy && make adoc)
