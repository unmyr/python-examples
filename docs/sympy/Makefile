BASE_DIR=../..
DOC_ROOT=..

DEST_DIR=$(BASE_DIR)/dist/sympy/
SRC_IMAGES_DIR=$(IMAGES_DIR)
DST_IMAGES_DIR=$(DEST_DIR)/$(IMAGES_DIR)

include $(DOC_ROOT)/asciidoc.mk

HTML_LIST=\
mkdir_and_copy \
$(DEST_DIR)/index.html

.PHONY: adoc mkdir_and_copy

adoc: $(HTML_LIST)

mkdir_and_copy:
	mkdir -p $(DEST_DIR)
	-test ! -d $(SRC_IMAGES_DIR) || mkdir -p $(DST_IMAGES_DIR)
	-test ! -d $(SRC_IMAGES_DIR) || cp $(CP_OPTS) $(SRC_IMAGES_DIR)/* $(DST_IMAGES_DIR)/

$(DEST_DIR)/%.html: %.adoc
	asciidoctor --trace $(AD_OPTS_HTML5_ROUGE) -o "$@" "$<"
