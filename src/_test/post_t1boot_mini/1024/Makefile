# GNU-make build for "post_t1boot_mini" -- a copy of t1_boot_fix/1024
# (NOT tlb_fix -- deliberately missing tlb_fix's own "tlb" node, kept
# that way on purpose for this experiment) with exactly four cpu/platform
# property changes added to test whether they alone are sufficient to
# clear illumos-gate's broken_md_flag=0 (strict) property-scan checks:
#
#   domaining-enabled = 1        (platform node -- flips broken_md_flag
#                                  to 0; see init_md_broken(), sun4v/os/
#                                  fillsysinfo.c)
#   mmu-page-size-list = 0xb     (was 0x9 in t1_boot_fix; 0xb is the
#                                  minimum value that clears cpu_setup()'s
#                                  strict-path check in niagara.c: mask
#                                  must already include 8K|64K|4M)
#   mmu-#context-bits = 0xd      (md-bindings.pdf documented default,
#                                  13 -- get_mmu_ctx_bits() panics on
#                                  absence OR on a declared value of 0,
#                                  regardless of broken_md_flag; this is
#                                  the one property in this set whose
#                                  panic path is NOT flag-gated at all)
#   q-cpu-mondo-#bits = 0x8, q-dev-mondo-#bits = 0x8, q-resumable-#bits = 0x6,
#   q-nonresumable-#bits = 0x2 -- real values, matching post_tlb_fix2 and
#   grounded in illumos's own DEFAULT_CPU_Q_ENTRIES(256)/DEFAULT_DEV_Q_ENTRIES(256)/
#   CPU_RQ_ENTRIES(64)/CPU_NRQ_ENTRIES(4) (sun4v/sys/machsystm.h, sun4v/sys/error.h).
#   Originally all four were deliberately left at 0x0 (degenerate 1-entry
#   queues) to test get_single_q_size()'s absence-only panic gate in
#   isolation; live kmdb testing of tlb_fix/1024 (broken_md_flag=1, real
#   values) confirmed hv_cpu_qconf() completes cleanly with sane sizes,
#   so this variant was updated to match once the degenerate-value
#   experiment had served its purpose. See docs/niagara-findings.md
#   (qemu-sparc64 project) for the live trace that motivated this.
#
# Deliberately excludes mmu-max-#tsbs and mmu-#shared-contexts -- traced
# as having identical (absent-tolerant, no panic) behavior regardless of
# broken_md_flag, so this experiment tests whether they're truly
# dispensable for getting through property-scanning.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/_test/post_t1boot_mini/1024/ tree (see OUT_DIR below), so src stays pure
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
# source -- sibling bin/post_t1boot_mini/1024/ directory.
OUT_DIR := ../../../../bin/_test/post_t1boot_mini/1024

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
