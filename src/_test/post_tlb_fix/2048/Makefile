# GNU-make build for the "post_tlb_fix" experimental variant of the
# tlb_fix 2048MB sun4v MD/hv-config -- a copy of src/tlb_fix/2048/ with
# one added change: the cpu node's mmu-page-size-list is widened from
# 0x9 (bits 0,3 = 8K, 4M) to 0x39 (bits 0,3,4,5 = 8K, 4M, 32M, 256M),
# unlocking the two largest page sizes for kernel use. The "cache" node
# is left bare (back -> cpu0 only), matching tlb_fix/2048 exactly --
# same as it was before an interim experiment briefly populated it with
# real L2 properties (level=2, associativity=0xc, size=0x300000,
# line-size=0x40) to test a separate hp_colors/ecache_setsize hypothesis;
# that's reverted here to keep this build isolated to the pagesize-list
# change alone.
#
# Deliberately isolated to just this one change (no cache-node changes,
# no tlb-node property changes, no max-cpus declaration) so it can be
# tested independently -- see docs/index.html test matrix.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/_test/post_tlb_fix/2048/ tree (see OUT_DIR below), so src stays pure
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
#   qemu-system-sparc64 -M niagara -L <OUT_DIR> -L ../../../../fw_blobs ...
#
# QEMU appends each -L to its data-dir list and searches them in declaration
# order; specifying an incomplete directory this way is exactly what that
# feature was added for (commit 4524051c32, "so you don't have to create a
# symlink farm for all the rom blobs"). Verify with -L help / -trace load_file.

# Built output (.bin/.txt) lands here, not alongside the
# source -- sibling bin/post_tlb_fix/2048/ directory.
OUT_DIR := ../../../../bin/_test/post_tlb_fix/2048

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
