#!/usr/bin/env python
from __future__ import print_function
import sys

utrlens = dict()
premrnas = open(sys.argv[1], 'r')
next(premrnas)
for line in premrnas:
    values = line.rstrip().split('\t')
    mrnaid = values[1]
    ulen = int(values[8]) + int(values[9])
    utrlens[mrnaid] = ulen

iloci = open(sys.argv[2], 'r')
header = next(iloci)
header = header.rstrip() + '\tUTRLength'
print(header)
for line in iloci:
    values = line.rstrip().split('\t')
    mrnaid = values[-1]
    if mrnaid == 'NA':
        utrlen = 0
    else:
        utrlen = utrlens[mrnaid]
    print(line.rstrip() + '\t%d' % utrlen)
