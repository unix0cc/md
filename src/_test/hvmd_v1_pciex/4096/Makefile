# GNU-make build for "pagesize_256m/4096" -- a copy of src/_test/pagesize_256m/2048/ with one
# changed property: mmu-page-size-list widened from 0x9 to 0x2b (adds the
# 64K and 256M bits: TTE8K|TTE64K|TTE4M|TTE256M).
#
# 4096MB variant of pagesize_256m/2048 -- only 1up.pdesc's mblock size and
# 1up.hdesc's GUEST() memsize (4th arg) changed to 4096M, both places kept in
# sync (see tlb_fix/4096's Makefile for why missing one silently caps the
# guest). common.pdesc/common.hdesc (incl. mmu-page-size-list=0x2b) unchanged.
#
# Purpose: live kmdb verification of the QEMU-side sun4v TTE page-size fix
# (target/sparc bit-48 szh placement, see qemu-sparc64 project's
# tte-pagesize-three-layers memory) requires a guest whose
# mmu_exported_pagesize_mask actually includes TTE256M, so alloc_kmem64()'s
# size-selection loop (uts/sun4/os/startup.c) can land on kmem64_szc=0x5
# instead of being capped at TTE4M by a narrower mask. tlb_fix/2048's
# declared 0x9 was observed live (2026-07-26) to result in an effective
# mmu_exported_pagesize_mask of 0xb at the alloc_kmem64 breakpoint -- still
# missing bit 5 -- so a config that gets 256M into the *effective* mask,
# not just survives broken_md_flag's DEFAULT_SUN4V_MMU_PAGESIZE_MASK(0xb)
# floor, is needed. 0x2b matches NI_MMU_PAGESIZE_MASK (sun4v/cpu/niagara.c)
# and is the same value the (abandoned) niagara-qemu gen-4 MD lineage
# declares.
#
# Flat layout (single "1up" config, no per-config subdirectory) -- unlike
# OpenSPARC_T1_rebuild/ and t1_boot_fix/256/, which wildcard-scan for multiple
# config subdirectories.
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/_test/hvmd_v1_pciex/4096/ tree (see OUT_DIR below), so src stays pure
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
# source -- sibling bin/_test/pagesize_256m/2048/ directory.
OUT_DIR := ../../../../bin/_test/hvmd_v1_pciex/4096

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
