#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import re
import sys
import fasta_utils


def get_args():
    desc = 'Retrieve sequences by ID from Fasta data.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file; default is terminal (stdout)')
    parser.add_argument('-l', '--line_width', type=int, default=80,
                        help='Max line width for sequences; default is 80 bp')
    parser.add_argument('idlist', type=argparse.FileType('r'))
    parser.add_argument('seqs', type=argparse.FileType('r'))
    return parser


def main(parser=get_args()):
    args = parser.parse_args()

    ids = dict()
    for line in args.idlist:
        seqid = line.rstrip()
        ids[seqid] = True

    for defline, seq in fasta_utils.parse_fasta(args.seqs):
        seqid = re.search('>(\S+)', defline).group(1)
        if seqid in ids:
            print >> args.out, defline
            fasta_utils.format_seq(seq, linewidth=args.line_width,
                                   outstream=args.out)

if __name__ == '__main__':
    main()
