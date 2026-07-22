# GNU-make port of the original OpenSPARC T1 "niagara" Legion MD/hv-config
# Makefile (legion/src/config/niagara/Makefile + ../Makefile.master).
#
# Ported from Sun Studio/Solaris make ($(TOP)/Makefile.master, hardcoded
# /usr/ccs/lib/cpp, $(SAM_ROOT)-relative mdgen path, .KEEP_STATE:) to plain
# GNU make. Source (.pdesc/.hdesc) is Sun's original, unmodified 2006
# OpenSPARC T1 release (GPLv2 -- see each file's own header; NOT the same
# license as the mdgen/mdlint tool source in github.com/unix0cc/mdbuild).
#
# Flat layout (single "1up" config, no per-config subdirectory) -- matches
# t1_boot_fix/1024/ and t1_boot_fix/2048/'s convention (2026-07-22
# restructuring; previously wildcard-scanned for multiple config
# subdirectories, but only "1up" was ever populated).
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt and firmware-blob symlinks into the sibling
# bin/OpenSPARC_T1_rebuild/ tree (see OUT_DIR below), so src stays
# pure source and bin stays pure blobs even right after a build.
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
# source -- sibling bin/OpenSPARC_T1_rebuild/ directory.
OUT_DIR := ../../bin/OpenSPARC_T1_rebuild

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
