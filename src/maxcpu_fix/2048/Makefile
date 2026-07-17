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
# writes built .bin/.txt and firmware-blob symlinks into the sibling
# bin/maxcpu_fix/2048/ tree (see OUT_DIR below), so src stays pure
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
# source -- sibling bin/maxcpu_fix/2048/ directory.
OUT_DIR := ../../../bin/maxcpu_fix/2048

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
