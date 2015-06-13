#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""
Compute a multiple sequence alignment for a hiLocus.
"""

import hilocus_utils


if __name__ == '__main__':
    import argparse
    import sys

    desc = 'Align proteins corresponding to a hiLocus'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--cpath', default=None,
                        help='path to dir containing clustalw program (if not '
                        'in $PATH)')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-o', '--out', default=None,
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
    hilocus_utils.run_msa(proteinseqs, outfile=args.out, path=args.cpath)
