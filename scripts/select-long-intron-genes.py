#!/usr/bin/env python
from __future__ import print_function
import argparse
import itertools
import re
import sys

desc = 'Identify gene models with long introns'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-l', '--length', type=int, default=50000, metavar='LEN',
                    help='Length at which an intron is considered "long"; '
                    'default is 50000')
parser.add_argument('-a', '--attr', default='ID', help='Attribute of matching '
                    'gene models to report; default is "ID"')
parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                    default=sys.stdout, help='File to which output will be '
                    'written; default is terminal (stdout)')
parser.add_argument('gff3', type=argparse.FileType('r'), nargs='+',
                    help='Input GFF3 file(s)')
args = parser.parse_args()

gff3in = args.gff3
if isinstance(args.gff3, list):
    gff3in = itertools.chain(*args.gff3)

feat_attrs = dict()
toreport = set()
for line in gff3in:
    fields = line.rstrip().split('\t')
    if len(fields) != 9:
        continue
    feattype = fields[2]
    attrs = fields[8]

    idmatch = re.search('ID=([^;\n]+)', attrs)
    if idmatch:
        featid = idmatch.group(1)
        feat_attrs[featid] = attrs

    if feattype != 'intron':
        continue

    start = int(fields[3])
    end = int(fields[4])
    length = end - start + 1
    if length < args.length:
        continue

    parentmatch = re.search('Parent=([^;\n]+)', attrs)
    assert parentmatch, 'intron without a parent feature: ' + attrs
    parentids = parentmatch.group(1)
    for parentid in parentids.split(','):
        assert parentid in feat_attrs, 'Feature ID=%s not found' % parentid
        parent_attrs = feat_attrs[parentid]
        regexp = '%s=([^;\n]+)' % args.attr
        attrmatch = re.search(regexp, parent_attrs)
        if attrmatch:
            attrval = attrmatch.group(1)
        else:
            print('warning: %s attribute not found for "%s", reporting ID '
                  'instead' % (args.attr, parentid), file=sys.stderr)
            attrval = parentid
        toreport.add(attrval)

for value in sorted(list(toreport)):
    print(value, file=args.out)
