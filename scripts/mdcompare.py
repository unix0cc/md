#!/usr/bin/env python3
"""Compare two binary MDESCs property by property.

Written to answer one question that inspection cannot: which of our deviations
from Sun's reference configuration are deliberate, and which are leftovers
nobody remembers. Every difference has to be classifiable, and to classify it
you first have to see all of them.

Nodes are matched by an identity built from the node type plus whichever of
`name`, `id` or `cfg-handle` it carries -- MD node names are not unique (a guest
MD has half a dozen `virtual-device` nodes), so the type alone will not do.

Usage: mdcompare.py OURS THEIRS [--label-a NAME --label-b NAME]
"""
import struct
import sys

TAGS = {b'N': 'node', b'E': 'end', b'a': 'arc', b'v': 'val',
        b's': 'str', b'd': 'data', b'\0': 'null'}


def parse(path):
    """Return [(identity, {prop: value}), ...] in file order."""
    b = open(path, 'rb').read()
    _ver, nsz, namesz, datasz = struct.unpack_from('>IIII', b, 0)
    nodes = b[16:16 + nsz]
    names = b[16 + nsz:16 + nsz + namesz]
    data = b[16 + nsz + namesz:16 + nsz + namesz + datasz]

    def cstr(blk, off):
        end = blk.find(b'\0', off)
        return blk[off:end].decode('latin1')

    out, cur, curname = [], None, None
    for i in range(len(nodes) // 16):
        tag, _nlen, _r, noff = struct.unpack_from('>BBHI', nodes, i * 16)
        raw = nodes[i * 16 + 8:i * 16 + 16]
        t = TAGS.get(bytes([tag]), '?')
        name = cstr(names, noff) if noff < len(names) else ''

        if t == 'node':
            cur, curname = {}, name
        elif t == 'end':
            if cur is not None:
                out.append((curname, cur))
            cur = None
        elif cur is not None:
            if t == 'val':
                cur[name] = '0x%x' % struct.unpack('>Q', raw)[0]
            elif t == 'str':
                _dlen, doff = struct.unpack('>II', raw)
                cur[name] = '"%s"' % cstr(data, doff)
            elif t == 'data':
                dlen, doff = struct.unpack('>II', raw)
                blob = data[doff:doff + dlen]
                if blob and all(32 <= c < 127 or c == 0 for c in blob):
                    parts = [p.decode('latin1') for p in blob.split(b'\0') if p]
                    cur[name] = '{ %s }' % ', '.join(parts)
                else:
                    cur[name] = '<%d bytes>' % dlen
            elif t == 'arc':
                cur.setdefault('(arcs)', [])
                cur['(arcs)'].append(name)
    return out


def identify(nodename, props):
    for key in ('name', 'id', 'cfg-handle', 'channel', 'resource_id'):
        if key in props:
            return '%s[%s=%s]' % (nodename, key, props[key])
    return nodename


def index(nodes):
    d = {}
    for nodename, props in nodes:
        ident = identify(nodename, props)
        while ident in d:            # duplicates: keep both, distinguishable
            ident += "'"
        d[ident] = props
    return d


def main():
    a_path, b_path = sys.argv[1], sys.argv[2]
    la, lb = 'OURS', 'SUN'
    if '--label-a' in sys.argv:
        la = sys.argv[sys.argv.index('--label-a') + 1]
    if '--label-b' in sys.argv:
        lb = sys.argv[sys.argv.index('--label-b') + 1]

    A, B = index(parse(a_path)), index(parse(b_path))

    only_a = [k for k in A if k not in B]
    only_b = [k for k in B if k not in A]
    both = [k for k in A if k in B]

    print('=' * 72)
    print('%s: %s' % (la, a_path))
    print('%s: %s' % (lb, b_path))
    print('=' * 72)

    if only_a:
        print('\n### nodes only in %s (%d)\n' % (la, len(only_a)))
        for k in sorted(only_a):
            print('  %s' % k)
    if only_b:
        print('\n### nodes only in %s (%d)\n' % (lb, len(only_b)))
        for k in sorted(only_b):
            print('  %s' % k)

    diffs = []
    for k in both:
        pa, pb = A[k], B[k]
        for prop in sorted(set(pa) | set(pb)):
            if prop == '(arcs)':
                continue          # arc targets are indices; compared by count
            va, vb = pa.get(prop), pb.get(prop)
            if va != vb:
                diffs.append((k, prop, va, vb))
    if diffs:
        print('\n### properties differing on nodes present in both (%d)\n' % len(diffs))
        print('  %-30s %-24s %-22s %s' % ('node', 'property', la, lb))
        print('  ' + '-' * 88)
        for k, prop, va, vb in diffs:
            print('  %-30s %-24s %-22s %s' % (k[:30], prop[:24],
                                              str(va)[:22], str(vb)))
    print('\n%d node(s) matched, %d only in %s, %d only in %s' %
          (len(both), len(only_a), la, len(only_b), lb))


if __name__ == '__main__':
    main()
