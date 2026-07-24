# GNU-make build for "post_tlb_fix2" -- a copy of src/post_tlb_fix/2048/
# (itself tlb_fix/2048 + domaining-enabled=1 + mmu-page-size-list=0xb +
# the four q-*-mondo-#bits) with three more cpu-node properties added to
# the ADD_CPU macro in common.pdesc, each set to md-bindings.pdf (FWARC
# 2005/115, Rev 0.18)'s own documented default value, rather than left
# absent as post_tlb_fix/2048 has them:
#
#   mmu-max-#tsbs        = 0x1  (spec default if absent is 1)
#   mmu-#context-bits    = 0xd  (spec default if absent is 13)
#   mmu-#shared-contexts = 0x0  (spec default if absent is 0)
#
# Motivation: illumos-gate's get_mmu_ctx_bits() (sun4v/os/fillsysinfo.c)
# has NO broken_md_flag bypass for a missing mmu-#context-bits -- it
# defaults to 0 internally and then panics an unconditional range check
# (0 < MIN_NCTXS_BITS=2). post_tlb_fix/2048 leaves it absent; this variant
# declares it explicitly so that code path can never be reached, whether
# or not broken_md_flag ends up set. The other two additions are lower-
# stakes (illumos silently defaults both to the same value if absent, no
# panic either way) but added for the same spec-conformance reason. See
# docs/niagara-findings.md's "tlb_fix/2048 post-watchdog hang" entry
# (qemu-sparc64 project) for the full property-by-property trace this
# was derived from.
#
# q-cpu-mondo-#bits/q-dev-mondo-#bits/q-resumable-#bits/q-nonresumable-#bits
# are carried over unchanged from post_tlb_fix/2048 (0x8/0x8/0x6/0x2) --
# already correct: get_single_q_size() treats the declared value as a bit
# count (actual entries = 1 << value), and 0x8/0x8/0x6/0x2 reproduce
# illumos's own DEFAULT_CPU_Q_ENTRIES(0x100)/DEFAULT_DEV_Q_ENTRIES(0x100)/
# CPU_RQ_ENTRIES(64)/CPU_NRQ_ENTRIES(4) exactly.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/_test/post_tlb_fix2/2048/ tree (see OUT_DIR below), so src stays pure
# source and bin stays pure blobs even right after a build.
#
# mdgen itself comes from github.com/unix0cc/mdbuild, built via that repo's
# own GNU Makefile -- not built here.

# NOTE: CPP is a GNU Make built-in variable (default "cc -E"); ?= would be
# silently ignored, so this must be an unconditional override.
CPP     := cpp -traditional-cpp
MDGEN   ?= $(HOME)/mdbuild/bin/mdgen
VERBOSE ?=

# Static OBP/firmware blobs (openboot.bin, q.bin, reset.bin, nvram1) are not
# part of a normal build. Pass fw_blobs/ to QEMU as a second search path:
#
#   qemu-system-sparc64 -M niagara -L <OUT_DIR> -L ../../../../fw_blobs ...
#
# QEMU appends each -L to its data-dir list and searches them in declaration
# order; specifying an incomplete directory this way is exactly what that
# feature was added for (commit 4524051c32, "so you don't have to create a
# symlink farm for all the rom blobs"). Verify with -L help / -trace load_file.
#
# `make symlinks` is the opt-in alternative, for when a single -L is wanted:
# it links the firmware into OUT_DIR so that one directory holds all six
# files. The links are relative, so they survive a move or a fresh clone,
# and .gitignore keeps them out of commits -- the absolute, committed
# symlink farm this repo used to carry is what commit 4524051c32 above
# describes not needing.
FW_BLOBS := ../../../../fw_blobs
FW_FILES := nvram1 openboot.bin q.bin reset.bin

# Built output (.bin/.txt) lands here, not alongside the
# source -- sibling bin/post_tlb_fix2/2048/ directory.
OUT_DIR := ../../../../bin/_test/post_tlb_fix2/2048

.PHONY: all symlinks clean distclean

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

# Opt-in: link the firmware into OUT_DIR so a single -L suffices. Relative
# link targets are computed from OUT_DIR, so they stay correct at any depth
# and in any clone. `make distclean` removes them along with OUT_DIR.
symlinks: all
	@for f in $(FW_FILES); do \
	    ln -sfn "$$(realpath --relative-to=$(OUT_DIR) $(FW_BLOBS)/$$f)" $(OUT_DIR)/$$f; \
	    echo "$(OUT_DIR)/$$f -> $$(readlink $(OUT_DIR)/$$f)"; \
	done

clean:
	$(RM) *.pp

distclean: clean
	$(RM) -r $(OUT_DIR)
