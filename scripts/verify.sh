#!/usr/bin/env bash
#
# verify.sh -- check that every committed config in bin/ is exactly what its
# source in src/ currently builds.
#
# The failure mode this guards against: somebody edits a .pdesc/.hdesc, forgets
# to run make, and commits. Git will not complain -- it simply shows a changed
# source and an unchanged blob -- but bin/<config>/ no longer corresponds to
# src/<config>/, which silently invalidates every boot result in
# docs/index.html and md-artefacts that cites that config.
#
# Each config is rebuilt into a temporary directory (make OUT_DIR=... overrides
# the Makefile's own setting) and compared against what is committed. Nothing
# under bin/ is written, moved or removed, so this is safe to run at any time,
# including with a dirty working tree.
#
# Exit status:
#   0  every config matches its source
#   1  at least one config drifted, failed to build, or has stray files
#   2  cannot verify (mdgen missing) -- deliberately not 0, so that "verify
#      passed" can never mean "verify never ran"
#
# Usage: scripts/verify.sh [-q]
#   -q  quiet: print only problems and the summary

set -u

REPO_ROOT=$(cd -- "$(dirname -- "$0")/.." && pwd)
MDGEN=${MDGEN:-$HOME/mdbuild/bin/mdgen}

quiet=0
case ${1:-} in
    -q) quiet=1 ;;
    -h|--help) sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    "") ;;
    *) echo "verify.sh: unknown argument '$1' (try --help)" >&2; exit 2 ;;
esac

if [ ! -x "$MDGEN" ]; then
    echo "verify.sh: cannot verify -- mdgen not found at $MDGEN" >&2
    echo "  build it from github.com/unix0cc/mdbuild, or set MDGEN=<path>" >&2
    exit 2
fi

tmpdirs=""
cleanup() { [ -n "$tmpdirs" ] && rm -rf $tmpdirs; }
trap cleanup EXIT INT TERM

rc=0
checked=0

for makefile in $(find "$REPO_ROOT/src" -name Makefile | sort); do
    srcdir=$(dirname "$makefile")
    label=${srcdir#"$REPO_ROOT"/src/}

    # OUT_DIR is declared in the Makefile, relative to the config directory.
    outrel=$(sed -n 's/^OUT_DIR[[:space:]]*:=[[:space:]]*//p' "$makefile" | head -1)
    if [ -z "$outrel" ]; then
        printf '%-40s NO OUT_DIR in Makefile\n' "$label"; rc=1; continue
    fi
    outdir=$(cd -- "$srcdir" && cd -- "$outrel" 2>/dev/null && pwd)
    if [ -z "$outdir" ]; then
        printf '%-40s output dir missing: %s\n' "$label" "$outrel"; rc=1; continue
    fi

    tmp=$(mktemp -d) || exit 2
    tmpdirs="$tmpdirs $tmp"

    if ! log=$(cd -- "$srcdir" && make OUT_DIR="$tmp" 2>&1); then
        printf '%-40s BUILD FAILED\n' "$label"
        printf '%s\n' "$log" | sed 's/^/    /'
        rc=1
        continue
    fi

    # What this config is *supposed* to contain is whatever the build just
    # produced -- taken from the temp directory rather than a fixed list, so
    # configs that build more than one MD (OpenSPARC_T1_rebuild builds 1up,
    # 1g2p and 1g32p) are handled without the script knowing their names.
    expected=""
    for built in "$tmp"/*; do
        [ -e "$built" ] || continue
        expected="$expected $(basename "$built")"
    done
    if [ -z "$expected" ]; then
        printf '%-40s BUILD PRODUCED NOTHING\n' "$label"; rc=1; continue
    fi

    drift=""
    for f in $expected; do
        cmp -s "$tmp/$f" "$outdir/$f" || drift="$drift $f"
    done

    # The config directory must hold the built artefacts and nothing else.
    # Firmware blobs used to be symlinked in here; they were dropped because
    # the links were absolute and so broke every clone outside /git/md, and
    # because a stray copy of a blob shadows later -L paths at run time.
    # (See CHANGELOG, 2026-07-23, for the full account.)
    stray=""
    for existing in "$outdir"/*; do
        [ -e "$existing" ] || continue
        base=$(basename "$existing")
        case " $expected " in
            *" $base "*) ;;
            *) stray="$stray $base" ;;
        esac
    done

    if [ -n "$drift" ] || [ -n "$stray" ]; then
        [ -n "$drift" ] && printf '%-40s DRIFT:%s\n' "$label" "$drift"
        [ -n "$stray" ] && printf '%-40s STRAY FILES:%s\n' "$label" "$stray"
        rc=1
    elif [ "$quiet" -eq 0 ]; then
        printf '%-40s ok\n' "$label"
    fi
    checked=$((checked + 1))
done

if [ "$checked" -eq 0 ]; then
    echo "verify.sh: no configs found under $REPO_ROOT/src" >&2
    exit 2
fi

# ---------------------------------------------------------------------------
# The byte-identity proof.
#
# OpenSPARC_T1_rebuild exists to demonstrate one thing: that our GNU-make port
# of mdgen reproduces the binaries Sun shipped in 2006, byte for byte. The loop
# above cannot show that -- it only proves bin/ matches what src/ currently
# builds, which stays true even if somebody edits the "verbatim" sources and
# rebuilds. Both legs have to be checked, or a green run means nothing here:
#
#   1. src/OpenSPARC_T1_rebuild/*.pdesc|hdesc  ==  Sun's originals
#   2. bin/OpenSPARC_T1_rebuild/*.bin          ==  Sun's originals
# ---------------------------------------------------------------------------
REF="$REPO_ROOT/bin/_reference/OpenSPARC_T1_original/niagara"
REBUILD_SRC="$REPO_ROOT/src/OpenSPARC_T1_rebuild"
REBUILD_BIN="$REPO_ROOT/bin/OpenSPARC_T1_rebuild"

if [ -d "$REF" ]; then
    refbad=""
    # All three configs Sun shipped. 1up alone is a weak proof: it is a
    # single-strand, single-guest machine, while 1g2p and 1g32p describe
    # multiple guests and 32 strands, reaching node and property shapes 1up
    # never does (1g32p-md.bin is 9104 bytes against 1up's 2408).
    for f in common.pdesc common.hdesc; do
        cmp -s "$REF/$f" "$REBUILD_SRC/$f" || refbad="$refbad src/$f"
    done
    for c in 1up 1g2p 1g32p; do
        for f in "$c.pdesc" "$c.hdesc"; do
            cmp -s "$REF/$f" "$REBUILD_SRC/$f" || refbad="$refbad src/$f"
        done
        for f in "$c-md.bin" "$c-hv.bin"; do
            cmp -s "$REF/$f" "$REBUILD_BIN/$f" || refbad="$refbad bin/$f"
        done
    done

    if [ -n "$refbad" ]; then
        printf '%-40s NOT BYTE-IDENTICAL TO SUN 2006:%s\n' "OpenSPARC_T1_rebuild" "$refbad"
        rc=1
    elif [ "$quiet" -eq 0 ]; then
        printf "%-40s byte-identical to Sun 2006 originals (1up, 1g2p, 1g32p)\n" "OpenSPARC_T1_rebuild"
    fi
else
    echo "verify.sh: reference originals missing at $REF" >&2
    rc=1
fi

if [ "$rc" -eq 0 ]; then
    echo "verify.sh: $checked config(s) match their source"
else
    echo "verify.sh: problems found (see above); $checked config(s) checked" >&2
fi
exit $rc
