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
                        help='path to dir containing clustalo program (if not '
                        'in $PATH)')
    parser.add_argument('-f', '--outfmt', default='clustal', metavar='FMT',
                        help='output format; default is clustal')
    parser.add_argument('-r', '--refmt', action='store_true',
                        help='reformat seqids so that they are short and '
                        'manageable (replace ID with species label)')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-o', '--out', default=None,
                        help='output file; default is terminal (stdout)')
    parser.add_argument('-M', action='store_true', help='Throw out any protein'
                        ' sequences that do not begin with a methionine (M)')
    parser.add_argument(default=None, dest='hid',
                        help='ID of the hiLocus for which protein MSA will '
                        'be generated')

    args = parser.parse_args()

    hilocus = hilocus_utils.load_hilocus(args.hid, rootdir=args.path)
    iloci = hilocus[5].split(',')
    species = hilocus[6].split(',')

    protids = hilocus_utils.resolve_protein_ids(iloci, species,
                                                rootdir=args.path)
    seqdata = list()
    for defline, seq in hilocus_utils.retrieve_proteins(protids, species,
                                                        rootdir=args.path):
        if args.M and not seq.startswith('M'):
            continue
        seqdata.extend((defline, seq))
    proteinseqs = '\n'.join(seqdata)
    hilocus_utils.run_msa(proteinseqs, outfile=args.out, path=args.cpath,
                          outfmt=args.outfmt, refmt=args.refmt)
