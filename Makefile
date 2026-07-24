# Top-level dispatcher. Every config under src/ has its own Makefile and can
# still be driven directly; this one just runs the same target across all of
# them, so that building or relinking the whole tree does not mean cd-ing
# through a dozen directories.
#
#   make                 build every config
#   make symlinks        link fw_blobs into every config (see README)
#   make clean           remove intermediates
#   make distclean       also remove built output under bin/
#   make verify          run scripts/verify.sh
#   make list            print the config names
#   make tlb_fix/1024    build one config by name
#
# MDGEN is passed straight through, so `make MDGEN=/path/to/mdgen` works here
# exactly as it does in a config directory.

CONFIGS := $(patsubst src/%/Makefile,%,$(shell find src -name Makefile | sort))

.PHONY: all symlinks clean distclean verify list $(CONFIGS)

all symlinks clean distclean:
	@for c in $(CONFIGS); do \
	    printf '==> %s\n' "$$c"; \
	    $(MAKE) --no-print-directory -C src/$$c $@ || exit 1; \
	done

# Build a single config: `make tlb_fix/1024`, `make OpenSPARC_T1_rebuild`.
$(CONFIGS):
	@$(MAKE) --no-print-directory -C src/$@

verify:
	@scripts/verify.sh

list:
	@printf '%s\n' $(CONFIGS)
