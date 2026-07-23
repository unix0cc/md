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
# writes built .bin/.txt into the sibling
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

# Static OBP/firmware blobs (openboot.bin, q.bin, reset.bin, nvram1) are
# deliberately NOT copied or symlinked into the output directory. Pass
# fw_blobs/ to QEMU as a second search path instead:
#
#   qemu-system-sparc64 -M niagara -L <OUT_DIR> -L ../../fw_blobs ...
#
# QEMU appends each -L to its data-dir list and searches them in declaration
# order; specifying an incomplete directory this way is exactly what that
# feature was added for (commit 4524051c32, "so you don't have to create a
# symlink farm for all the rom blobs"). Verify with -L help / -trace load_file.

# Built output (.bin/.txt) lands here, not alongside the
# source -- sibling bin/OpenSPARC_T1_rebuild/ directory.
OUT_DIR := ../../bin/OpenSPARC_T1_rebuild

# All three configs Sun shipped, same list and same pattern rules as their
# original niagara/Makefile ("CONFIGS = 1up 1g32p 1g2p"). Building all three
# widens the byte-identity proof: 1up is a single-strand, single-guest
# machine, while 1g2p and 1g32p describe multiple guests and 32 strands, so
# they exercise node and property shapes 1up never reaches.
CONFIGS := 1up 1g2p 1g32p

OUTPUTS := $(foreach c,$(CONFIGS),\
	$(OUT_DIR)/$(c)-md.bin $(OUT_DIR)/$(c)-md.txt \
	$(OUT_DIR)/$(c)-hv.bin $(OUT_DIR)/$(c)-hv.txt)

.PHONY: all clean distclean

all: $(OUTPUTS)

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
