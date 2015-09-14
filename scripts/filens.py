#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('species', help='4-letter species label')
parser.add_argument('gff3', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

for line in args.gff3:
    liilmatch = re.search('liil=(\d+)', line)
    riilmatch = re.search('riil=(\d+)', line)
    idmatch = re.search('ID=([^;\n]+)', line)
    if not liilmatch or not riilmatch:
        continue

    lid = idmatch.group(1)
    liil = liilmatch.group(1)
    riil = riilmatch.group(1)
    fields = '\t'.join([args.species, lid, liil, riil])
    print(fields)
