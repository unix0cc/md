#!/usr/bin/env python3
"""mdesc.py - parse/patch sun4v MDESC blobs (guest MD like 1up-md.bin, or hv-config like 1up-hv.bin).

Usage:
  mdesc.py parse  <file>                          dump node/property tree with value file-offsets
  mdesc.py setval <file> <offset> <hexval> [out]  patch the 8-byte big-endian inline value at
                                                  <offset> (same length -> preserves all offsets),
                                                  writing to <out> (default <file>.patched).

Format: 16B big-endian header {ver=0x10000, node_blk, name_blk, data_blk}; then node block
(16B elements, tags N=node E=end v=val(inline u64) s=str d=data a=arc), name block, data block.
file_size == 16 + node + name + data.
"""
import sys, struct

def blocks(d):
    ver, node, name, data = struct.unpack(">IIII", d[:16])
    return ver, node, name, data, 16, 16 + node, 16 + node + name

def parse(fn):
    d = open(fn, "rb").read()
    ver, node, name, data, NB, NAMEB, DATAB = blocks(d)
    assert ver == 0x10000, "not MDESC (ver=%#x)" % ver
    assert len(d) == 16 + node + name + data, "block sizes don't sum to file size"
    nm = lambda o, l: d[NAMEB + o:NAMEB + o + l].split(b'\x00')[0].decode('latin1')
    depth = 0
    for e in range(node // 16):
        b = NB + e * 16; tag = d[b]; nlen = d[b + 1]
        noff = struct.unpack(">I", d[b + 4:b + 8])[0]
        val = struct.unpack(">Q", d[b + 8:b + 16])[0]
        if   tag == 0x4e: print("  " * depth + "NODE %s" % nm(noff, nlen)); depth += 1
        elif tag == 0x45: depth -= 1; print("  " * depth + "END")
        elif tag == 0x76: print("  " * depth + "val  %-14s = 0x%x (%d)   [off=%d]" % (nm(noff, nlen), val, val, b + 8))
        elif tag == 0x73:
            dl = struct.unpack(">I", d[b + 8:b + 12])[0]; do = struct.unpack(">I", d[b + 12:b + 16])[0]
            s = d[DATAB + do:DATAB + do + dl].split(b'\x00')[0].decode('latin1')
            print("  " * depth + "str  %-14s = %r   [data_off=%d len=%d]" % (nm(noff, nlen), s, DATAB + do, dl))
        elif tag == 0x64:
            dl = struct.unpack(">I", d[b + 8:b + 12])[0]
            print("  " * depth + "data %-14s (len %d)" % (nm(noff, nlen), dl))
        elif tag == 0x61: print("  " * depth + "arc  %-14s -> %d" % (nm(noff, nlen), val))
        elif tag == 0x00: break
        else: print("  " * depth + "?tag=0x%x %s" % (tag, nm(noff, nlen)))

def setval(fn, off, hexval, out):
    d = bytearray(open(fn, "rb").read())
    ver, node, name, data, _, _, _ = blocks(d)
    assert len(d) == 16 + node + name + data, "not a valid MDESC blob"
    old = struct.unpack(">Q", d[off:off + 8])[0]
    new = int(hexval, 0)
    d[off:off + 8] = struct.pack(">Q", new)
    assert len(d) == 16 + node + name + data, "size invariant broken"
    open(out, "wb").write(d)
    print("%s: [off %d] 0x%x -> 0x%x  written to %s" % (fn, off, old, new, out))

a = sys.argv
if   len(a) >= 3 and a[1] == "parse":  parse(a[2])
elif len(a) >= 5 and a[1] == "setval": setval(a[2], int(a[3], 0), a[4], a[5] if len(a) >= 6 else a[2] + ".patched")
else: print(__doc__); sys.exit(1)
