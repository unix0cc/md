# GNU-make build for the t1_boot_fix 256MB sun4v MD/hv-config, built from the
# original OpenSPARC T1 "niagara" Legion sources plus the fix patches in
# patches/t1_boot_fix/ (memory/cpus/cache nodes + mmu-* platform props --
# see patches/t1_boot_fix/separate-patches/ for the incremental chain).
#
# Flat layout (single "1up" config, no per-config subdirectory) -- matches
# t1_boot_fix/1024/ and t1_boot_fix/2048/'s convention (2026-07-22
# restructuring; previously wildcard-scanned for multiple config
# subdirectories, but only "1up" was ever populated).
#
# This directory holds ONLY source (.pdesc/.hdesc) + this Makefile. `make`
# writes built .bin/.txt into the sibling
# bin/t1_boot_fix/256/ tree (see OUT_DIR below), so src stays pure
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
#   qemu-system-sparc64 -M niagara -L <OUT_DIR> -L ../../../fw_blobs ...
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
FW_BLOBS := ../../../fw_blobs
FW_FILES := nvram1 openboot.bin q.bin reset.bin

# Built output (.bin/.txt) lands here, not alongside the
# source -- sibling bin/t1_boot_fix/256/ directory.
OUT_DIR := ../../../bin/t1_boot_fix/256

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
