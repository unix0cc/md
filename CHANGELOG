# Changelog

Notable changes to the MD/hv-config content and tooling in this repo. Newest
first. Cosmetic tweaks to `docs/index.html` (wording, formatting) are omitted;
see `git log` for those.

The blobs in `bin/` are built output, committed deliberately (they are the
evidence the boot matrix and `md-artefacts` cite). "byte-identical" below always
means verified with `scripts/verify.sh`, which rebuilds each config and compares.

## 2026-07-23

### Added
- `scripts/verify.sh` — rebuilds every config into a temp directory and compares
  against what is committed, catching source/blob drift (edit a `.pdesc`, forget
  to `make`, commit — git shows a changed source next to an unchanged blob and
  says nothing). Also re-checks the `OpenSPARC_T1_rebuild` byte-identity proof
  against `bin/_reference/`, flags stray files in a config dir, and exits 2 (not
  0) when it cannot run at all. Safe to run any time; writes nothing under `bin/`.

### Changed
- **Firmware is now passed as a second `-L`, not symlinked into each config.**
  Every `bin/<config>/` had carried `openboot.bin`/`q.bin`/`reset.bin`/`nvram1`
  (and an unused `netcons`) as symlinks into `fw_blobs/`. The links were
  **absolute** (`/git/md/fw_blobs/...`), so all 55 dangled in any clone outside
  `/git/md` — no config worked out of the box for anyone but the author. They
  were also unnecessary: QEMU's `-L` may be repeated and is searched in order
  (commit `4524051c32`, added in 2013 precisely "so you don't have to create a
  symlink farm for all the rom blobs"). A config dir now holds only its built
  blobs; invoke with `-L <config> -L fw_blobs`. The `fw-blobs` machinery is gone
  from every Makefile. **First-match-wins caveat:** a dir carrying its own copy
  of a blob shadows every `-L` after it — check with `-L help` / `-trace load_file`.
- **`OpenSPARC_T1_rebuild` now builds all three configs Sun shipped** — `1up`,
  `1g2p`, `1g32p` — instead of `1up` alone, matching the `CONFIGS` list in Sun's
  own `niagara/Makefile`. `1up` is a single-strand, single-guest machine and on
  its own exercised only a fraction of `mdgen`; `1g32p-md.bin` is 9104 bytes to
  `1up`'s 2408. All six blobs rebuild byte-identical to Sun's originals, widening
  the toolchain-fidelity proof from one config to three. `verify.sh`'s
  drift/stray checks were generalised off a hardcoded `1up-*` list at the same
  time.
- Makefile usage-comment paths for `fw_blobs` made relative (they had named the
  author-only absolute `/git/md/fw_blobs`).

## Earlier

The founding content: Sun's unmodified 2006 sources under
`bin/_reference/OpenSPARC_T1_original/`, the `OpenSPARC_T1_rebuild` byte-identity
proof, and the boot-fix patch chain — `t1_boot_fix` (memory/cpus/cache nodes +
`mmu-page-size-list`/`mmu-#va-bits` platform props, the live-kmdb-proven-minimal
set for a clean sun4v boot on illumos/OpenSolaris snv_134) and `tlb_fix` (adds a
per-cpu `tlb` node). See `patches/` for the reviewable diffs and `docs/index.html`
for the boot matrix.
