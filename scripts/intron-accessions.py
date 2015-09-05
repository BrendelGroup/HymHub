#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import sys
import re

rnatypes = ['mRNA', 'tRNA', 'ncRNA', 'transcript', 'primary_transcript']
rnaid_to_accession = dict()
for line in sys.stdin:
    line = line.rstrip()
    for rnatype in rnatypes:
        if ('\t%s\t' % rnatype) in line:
            accmatch = re.search('accession=([^;\n]+)', line)
            assert accmatch, 'Unable to parse transcript accession: %s' % line
            tid = re.search('ID=([^;\n]+)', line).group(1)
            rnaid_to_accession[tid] = accmatch.group(1)

    if '\tintron\t' in line:
        parentid = re.search('Parent=([^;\n]+)', line).group(1)
        assert ',' not in parentid, parentid
        accession = rnaid_to_accession[parentid]
        line += ';accession=%s' % accession

    print line
