#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import sys
import cdhit
import hilocus_utils


if __name__ == "__main__":
    """Script for creating HymHub's hiLocus data table."""

    desc = 'Parse CD-HIT output to determine hiLoci'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout, dest='outfile',
                        help='output file name; default is terminal (stdout)')
    parser.add_argument('-m', '--mint', type=str, default=None,
                        metavar='format', help='Mint unique IDs for each '
                        'hiLocus with the given printf-style format')
    parser.add_argument('cdhitfile', type=argparse.FileType('r'),
                        help='protein clustering (output file from CD-HIT)')
    parser.add_argument('mapping', type=argparse.FileType('r'), help='mapping '
                        'of protein IDs/accessions to iLocus IDs')
    args = parser.parse_args()

    prot2loci = dict()
    for line in args.mapping:
        protid, locid = line.rstrip().split('\t')
        prot2loci[protid] = locid

    header = ['iLocusCount', 'SpeciesCount',
              'PhylogeneticClassification', 'iLoci', 'Species']
    if args.mint is not None:
        header = ['ID', 'Label'] + header
        count = 0
    print >> args.outfile, '\t'.join(header)
    for clusterid, clusterseqs in cdhit.parse_clusters(args.cdhitfile):
        hl = hilocus_utils.hiLocus(clusterseqs, prot2loci)
        if args.mint is not None:
            count += 1
            uid = args.mint % count
            args.outfile.write('%s\t%s\t' % (uid, uid))
        args.outfile.write('%s\n' % hl)
