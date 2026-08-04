#!/usr/bin/env python3
"""Dump a binary MDESC to readable text.

Format: 16-byte header (transport_version, node_blk_sz, name_blk_sz,
data_blk_sz, all big-endian u32), then the node block of 16-byte elements,
then the name block, then the data block.

Element: tag(u8) name_len(u8) _rsvd(u16) name_off(u32) then 8 bytes that are
either a u64 value / next-index, or a (data_len, data_off) pair.
"""
import struct
import sys

TAGS = {b'N': 'node', b'E': 'end', b'a': 'arc', b'v': 'val',
        b's': 'str', b'd': 'data', b'\0': 'null'}


def load(path):
    b = open(path, 'rb').read()
    _ver, nsz, namesz, datasz = struct.unpack_from('>IIII', b, 0)
    nodes = b[16:16 + nsz]
    names = b[16 + nsz:16 + nsz + namesz]
    data = b[16 + nsz + namesz:16 + nsz + namesz + datasz]
    return nodes, names, data


def cstr(blk, off):
    end = blk.find(b'\0', off)
    return blk[off:end].decode('latin1')


def dump(path, only=None):
    nodes, names, data = load(path)
    n = len(nodes) // 16
    depth = 0
    printing = only is None
    for i in range(n):
        tag, nlen, _r, noff = struct.unpack_from('>BBHI', nodes, i * 16)
        raw = nodes[i * 16 + 8:i * 16 + 16]
        t = TAGS.get(bytes([tag]), '?%02x' % tag)
        name = cstr(names, noff) if noff < len(names) else ''

        if t == 'node':
            if only is not None:
                printing = name in only
            if printing:
                print('%s[%d] node %s {' % ('  ' * depth, i, name))
            depth += 1
        elif t == 'end':
            depth = max(0, depth - 1)
            if printing:
                print('%s}' % ('  ' * depth))
            if only is not None and depth == 0:
                printing = False
        elif printing:
            pad = '  ' * depth
            if t == 'val':
                v, = struct.unpack('>Q', raw)
                print('%s%s = 0x%x  (%d)' % (pad, name, v, v))
            elif t == 'arc':
                v, = struct.unpack('>Q', raw)
                print('%s%s -> [%d]' % (pad, name, v))
            elif t == 'str':
                dlen, doff = struct.unpack('>II', raw)
                print('%s%s = "%s"' % (pad, name, cstr(data, doff)))
            elif t == 'data':
                dlen, doff = struct.unpack('>II', raw)
                blob = data[doff:doff + dlen]
                if blob and all(32 <= c < 127 or c == 0 for c in blob):
                    parts = [p.decode('latin1')
                             for p in blob.split(b'\0') if p]
                    print('%s%s = { %s }' % (pad, name,
                                             ', '.join('"%s"' % p for p in parts)))
                else:
                    print('%s%s = <%d bytes> %s' % (pad, name, dlen,
                                                    blob[:16].hex()))


if __name__ == '__main__':
    dump(sys.argv[1], set(sys.argv[2:]) or None)
