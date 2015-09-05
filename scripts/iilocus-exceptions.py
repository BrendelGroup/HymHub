#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import re
import sys


if __name__ == '__main__':
    import argparse

    desc = ('Tabulate data about iiLocus exceptions in the given GFF3 file(s)')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-l', '--labels', nargs='+', default=[], help='label '
                        'for each file; by default, file name is used')
    parser.add_argument('iloci', type=argparse.FileType('r'), nargs='+',
                        default=sys.stdin, help='iLocus GFF3 file(s)')
    args = parser.parse_args()
    if args.labels:
        assert len(args.labels) == len(args.iloci)
    else:
        args.labels = [gff3file.name for gff3file in args.iloci]

    exception_types = ['complex-overlap', 'delta-overlap-delta',
                       'delta-overlap-gene', 'delta-re-extend',
                       'gene-contain-gene', 'gene-overlap-gene',
                       'intron-gene', 'fragmentation', 'gene-count']
    print('\t'.join(['Label'] + exception_types))
    for gff3file, label in zip(args.iloci, args.labels):
        exception_counts = dict((etype, 0) for etype in exception_types)
        annotated_seqs = dict()
        for entry in gff3file:
            if '\tgene\t' in entry and len(entry.split('\t')) == 9:
                exception_counts['gene-count'] += 1

            if '\tlocus\t' not in entry or len(entry.split('\t')) != 9:
                continue
            if 'unannot=true' in entry:
                continue
            seqid = entry.split('\t')[0]
            if seqid not in annotated_seqs:
                annotated_seqs[seqid] = True
                exception_counts['fragmentation'] += 1
            excmatch = re.search('iiLocus_exception=([^;\n]+)', entry)
            if not excmatch:
                continue
            typestr = excmatch.group(1)
            complexmatch = re.search('complex-overlap-(\d+)', typestr)
            if complexmatch:
                numgenes = int(complexmatch.group(1))
                iiloci_missing = numgenes - 1
                exception_counts['complex-overlap'] += iiloci_missing
            else:
                exception_counts[typestr] += 1
        exvals = ['%d' % exception_counts[etyp] for etyp in exception_types]
        print('\t'.join([label] + exvals))
