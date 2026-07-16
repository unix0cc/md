# GNU-make build for the snv136 1024MB sun4v MD/hv-config, built from the
# original OpenSPARC T1 "niagara" Legion sources plus the fix patches in
# md_hv_patches/snv_136/ (memory/cpus/cache nodes + mmu-* platform props),
# with mblock.size/GUEST() memsize bumped to 1024M (see common two-layer
# memory model: MD mblock.size and hv-config GUEST() memsize must both
# match the QEMU -m flag).
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and snv136/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt and firmware-blob symlinks into the sibling
# md_hv_blobs/snv136/1024/ tree (see OUT_DIR below), so md_hv stays pure
# source and md_hv_blobs stays pure blobs even right after a build.
#
# mdgen itself comes from github.com/unix0cc/mdbuild, built via that repo's
# own GNU Makefile -- not built here.

# NOTE: CPP is a GNU Make built-in variable (default "cc -E"); ?= would be
# silently ignored, so this must be an unconditional override.
CPP     := cpp -traditional-cpp
MDGEN   ?= $(HOME)/mdbuild/bin/mdgen
VERBOSE ?=

# Static OBP/firmware support blobs (openboot.bin, q.bin, reset.bin,
# nvram1, netcons -- not built by mdgen, just symlinked alongside the
# built md/hv binaries so a config directory has everything it needs).
FW_BLOBS := /git/md_blobs/fw_blobs

# Built output (.bin/.txt/firmware-symlinks) lands here, not alongside the
# source -- sibling md_hv_blobs/snv136/1024/ directory.
OUT_DIR := ../../../md_hv_blobs/snv136/1024

FW_BLOB_FILES := $(notdir $(wildcard $(FW_BLOBS)/*))
FW_BLOB_LINKS := $(foreach f,$(FW_BLOB_FILES),$(OUT_DIR)/$(f))

.PHONY: all clean distclean fw-blobs

all: $(OUT_DIR)/1up-md.bin $(OUT_DIR)/1up-md.txt $(OUT_DIR)/1up-hv.bin $(OUT_DIR)/1up-hv.txt fw-blobs

fw-blobs: $(FW_BLOB_LINKS)

$(FW_BLOB_LINKS):
	@mkdir -p $(dir $@)
	ln -sf $(FW_BLOBS)/$(notdir $@) $@

%-md.pp: %.pdesc
	$(CPP) $< $@

%-hv.pp: %.hdesc
	$(CPP) $< $@

$(OUT_DIR)/%-md.bin: %-md.pp
	@mkdir -p $(dir $@)
	$(MDGEN) --binary $(VERBOSE) --outfile $@ $<

$(OUT_DIR)/%-md.txt: %-md.pp
	@mkdir -p $(dir $@)
	$(MDGEN) --text --outfile $@ $<

$(OUT_DIR)/%-hv.bin: %-hv.pp
	@mkdir -p $(dir $@)
	$(MDGEN) --binary $(VERBOSE) --outfile $@ $<

$(OUT_DIR)/%-hv.txt: %-hv.pp
	@mkdir -p $(dir $@)
	$(MDGEN) --text --outfile $@ $<

clean:
	$(RM) *.pp

distclean: clean
	$(RM) -r $(OUT_DIR)
