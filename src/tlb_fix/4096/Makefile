# GNU-make build for the "tlb_fix" experimental variant of the t1_boot_fix
# 4096MB sun4v MD/hv-config -- a copy of src/tlb_fix/2048/ (itself derived
# from t1_boot_fix/2048) bumped to 4096MB, to test whether the bop_alloc_chunk
# OOM panic hit by sol-11_1-ai-sparc.iso against tlb_fix/2048 is genuine
# memory exhaustion (root-caused via live kmdb: OBP's boot-time allocator
# exhausts a shrink-and-retry loop down to 8KB granularity and still can't
# get memory) rather than a logic bug -- if so, more memory should clear it.
#
# IMPORTANT: this build's memory size is declared in TWO places that must
# both match the QEMU -m flag: this file's 1up.pdesc mblock.size, AND
# 1up.hdesc's GUEST() macro's 4th argument (memsize). Missing the hdesc
# side is exactly the bug that invalidated every tlb_fix/2048 test result
# earlier in this build's history (hv-config silently capped the guest at
# 1024M despite the MD and -m flag both claiming 2048M) -- both are set to
# 4096M here, double-checked against each other before building.
#
# See docs/index.html test matrix for which OS images hit which panics.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt and firmware-blob symlinks into the sibling
# bin/tlb_fix/4096/ tree (see OUT_DIR below), so src stays pure
# source and bin stays pure blobs even right after a build.
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
FW_BLOBS := /git/md/fw_blobs

# Built output (.bin/.txt/firmware-symlinks) lands here, not alongside the
# source -- sibling bin/tlb_fix/4096/ directory.
OUT_DIR := ../../../bin/tlb_fix/4096

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
