#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""Grab protein sequences for a hiLocus"""

import hilocus_utils


if __name__ == '__main__':
    import argparse
    import re
    import sys

    desc = 'Grab protein sequences a hiLocus'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-o', '--out', default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='output file; default is terminal (stdout)')
    parser.add_argument(default=None, dest='hid',
                        help='ID of the hiLocus for which protein MSA will '
                        'be generated')

    args = parser.parse_args()

    hilocus = hilocus_utils.load_hilocus(args.hid, rootdir=args.path)
    iloci = hilocus[5].split(',')
    species = hilocus[6].split(',')

    protids = hilocus_utils.resolve_protein_ids(iloci, species,
                                                rootdir=args.path)
    proteinseqs = hilocus_utils.load_proteins(protids, species,
                                              rootdir=args.path)
    proteinseqs = re.sub(r'>(gnl\|(....)\|\S+)', r'>\2 \1', proteinseqs)
    print >> args.out, proteinseqs
