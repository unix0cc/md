# GNU-make build for the "maxcpu_fix" experimental variant of the
# t1_boot_fix 2048MB sun4v MD/hv-config -- a copy of src/tlb_fix/2048/
# (which already has the tlb-node fix) with one added property: a
# declared "max-cpus = 1;" on the platform node.
#
# This tests Proposal B from the Level-14-interrupt/alloc_page_freelists
# investigation: our MD never declares "max-cpus", so the kernel's
# get_q_sizes()/get_single_q_size() (usr/src/uts/sun4v/os/fillsysinfo.c)
# falls back to the compile-time NCPU constant for ncpu_guest_max, giving
# a generous max_qsize (= ncpu_guest_max * 8) for the CPU mondo interrupt
# queue. Declaring the honest single-strand "max-cpus = 1" clamps that
# ceiling down to just 1*8 = 8 entries for q-cpu-mondo-#bits specifically
# (the only one of the four q-*-mondo-#bits queues scaled by CPU count) --
# a real behavior change, kept as its own separate experimental build
# rather than folded into tlb_fix/2048, to isolate whether this helps or
# hurts the alloc_page_freelists-adjacent Level-14 interrupt hang seen on
# tlb_fix/2048 at 2048M specifically.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/_test/maxcpu_fix/2048/ tree (see OUT_DIR below), so src stays pure
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
# source -- sibling bin/_test/maxcpu_fix/2048/ directory.
OUT_DIR := ../../../../bin/_test/maxcpu_fix/2048

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
