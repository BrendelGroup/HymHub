#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import sys
import hilocus_utils


def load_hilocus_data(infile):
    """Load phyloclass for each iLocus from hiLocus data table."""
    ilocus_class = dict()
    next(infile)
    for line in args.hiloci:
        values = line.rstrip().split('\t')
        phyloclass = values[4]
        iloci = values[5].split(',')
        for ilocus in iloci:
            ilocus_class[ilocus] = phyloclass
    return ilocus_class


def load_conserved_iloci(infile):
    """Load iLoci from conserved hiLocus data table."""
    hicons = dict()
    next(args.hicons)
    for line in args.hicons:
        values = line.split('\t')
        hicons[values[1]] = values[0]
    return hicons


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('Use iLocus information to provide a breakdown of genome content')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--counts', action='store_true',
                        help='report iLocus counts for each category; default '
                        'is to report total bp occupied')
    parser.add_argument('-f', '--skip_fragments', action='store_true',
                        help='ignore fragment iLoci')
    parser.add_argument('-r', '--rootdir', default='.',
                        help='path to HymHub root directory; default is '
                        'current directory')
    parser.add_argument('iloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='iLocus data table')
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='hiLocus data table')
    parser.add_argument('hicons', type=argparse.FileType('r'),
                        default=sys.stdin, help='conserved hiLocus data table')
    args = parser.parse_args()

    simple = hilocus_utils.load_simple_iloci(args.rootdir)
    ilocus_class = load_hilocus_data(args.hiloci)
    hicons = load_conserved_iloci(args.hicons)

    outcols = ['Conserved', 'Matched', 'Orphan', 'Complex', 'ncRNA',
               'Intergenic']
    breakdown = dict()
    next(args.iloci)
    for line in args.iloci:
        values = line.rstrip().split('\t')
        species = values[0]
        ilcid = values[1]
        ilclass = values[7]
        genecount = int(values[8])
        fragment = values[9]
        if args.skip_fragments and fragment == 'True':
            continue

        if species not in breakdown:
            breakdown[species] = dict((col, list()) for col in outcols)

        if ilclass == 'intron_gene':
            pass
        elif ilcid in hicons:
            assert genecount == 1, ilcid
            assert ilclass in ['mRNA', 'mixed'], ilcid
            breakdown[species]['Conserved'].append(values)
        elif ilclass == 'geneless':
            assert genecount == 0
            breakdown[species]['Intergenic'].append(values)
        elif ilclass == 'ncRNA' or ilclass == 'tRNA':
            breakdown[species]['ncRNA'].append(values)
        elif genecount > 1 or ilclass == 'mixed' or ilcid not in ilocus_class:
            breakdown[species]['Complex'].append(values)
        else:
            assert genecount == 1
            if ilocus_class[ilcid] == 'Orphan':
                breakdown[species]['Orphan'].append(values)
            else:
                # print('DEBUG matched: %s' % ilcid)
                breakdown[species]['Matched'].append(values)

    print('\t'.join(['Species'] + outcols))
    for species in sorted(breakdown):
        print(species, end='', sep='')
        for col in outcols:
            iloci = breakdown[species][col]
            if args.counts:
                print('\t%d' % len(iloci), end='', sep='')
            else:
                cumlength = sum([int(x[3]) - int(x[11]) for x in iloci])
                print('\t%d' % cumlength, end='', sep='')
        print('\n', end='')
