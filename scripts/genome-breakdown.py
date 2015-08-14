#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import sys
import hilocus_utils


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('Use iLocus information to provide a breakdown of genome content')
    parser = argparse.ArgumentParser(description=desc)
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

    # ilocus_mapping = ilocus_isoforms(rootdir=args.rootdir)
    simple = hilocus_utils.load_simple_iloci(args.rootdir)

    ilocus_class = dict()
    ilocus_hilocus = dict()
    next(args.hiloci)
    for line in args.hiloci:
        values = line.rstrip().split('\t')
        hilocusid = values[0]
        phyloclass = values[4]
        iloci = values[5].split(',')
        for ilocus in iloci:
            ilocus_class[ilocus] = phyloclass
            ilocus_hilocus[ilocus] = hilocusid

    hicons = dict()
    next(args.hicons)
    for line in args.hicons:
        values = line.split('\t')
        hicons[values[1]] = values[0]

    outcols = ['HymCons', 'Conserved', 'Orphan', 'Complex', 'ncRNA',
               'Intergenic']
    breakdown = dict()
    next(args.iloci)
    for line in args.iloci:
        values = line.rstrip().split('\t')
        species = values[0]
        ilcid = values[1]
        ilclass = values[7]
        genecount = int(values[8])
        if species not in breakdown:
            breakdown[species] = dict((col, list()) for col in outcols)

        if ilclass == 'geneless':
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
            elif ilcid in hicons:
                breakdown[species]['HymCons'].append(values)
            else:
                breakdown[species]['Conserved'].append(values)

    print('\t'.join(['Species'] + outcols))
    for species in sorted(breakdown):
        print(species, end='', sep='')
        for col in outcols:
            iloci = breakdown[species][col]
            cumlength = sum([int(x[3]) - int(x[11]) for x in iloci])
            print('\t%d' % cumlength, end='', sep='')
        print('\n', end='')
