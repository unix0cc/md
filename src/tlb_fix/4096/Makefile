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
# writes built .bin/.txt into the sibling
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

# Static OBP/firmware blobs (openboot.bin, q.bin, reset.bin, nvram1) are
# deliberately NOT copied or symlinked into the output directory. Pass
# fw_blobs/ to QEMU as a second search path instead:
#
#   qemu-system-sparc64 -M niagara -L <OUT_DIR> -L /git/md/fw_blobs ...
#
# QEMU appends each -L to its data-dir list and searches them in declaration
# order; specifying an incomplete directory this way is exactly what that
# feature was added for (commit 4524051c32, "so you don't have to create a
# symlink farm for all the rom blobs"). Verify with -L help / -trace load_file.

# Built output (.bin/.txt) lands here, not alongside the
# source -- sibling bin/tlb_fix/4096/ directory.
OUT_DIR := ../../../bin/tlb_fix/4096

.PHONY: all clean distclean

all: $(OUT_DIR)/1up-md.bin $(OUT_DIR)/1up-md.txt $(OUT_DIR)/1up-hv.bin $(OUT_DIR)/1up-hv.txt

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
