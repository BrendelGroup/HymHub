#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import sys
import hym_species
import hilocus_utils


def locus_mrna_map(root='.'):
    locus2mrna = dict()
    for species in hym_species.labels:
        fname = '%s/species/%s/%s.ilocus.mrnas.txt' % (root, species, species)
        for line in open(fname, 'r'):
            ilocusid, mrnaid = line.rstrip().split()
            locus2mrna[ilocusid] = mrnaid
    return locus2mrna


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
    parser.add_argument('-t', '--table', action='store_true',
                        help='print table with an extra column')
    parser.add_argument('-r', '--rootdir', default='.',
                        help='path to HymHub root directory; default is '
                        'current directory')
    parser.add_argument('-s', '--skiplong', action='store_true',
                        help='Skip 100 longest piLoci for all species')
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
               'Intergenic', 'Fragment']
    breakdown = dict()
    pilocus_lengths = dict()
    header = next(args.iloci)
    for line in args.iloci:
        values = line.rstrip().split('\t')
        species = values[0]
        ilcid = values[1]
        eff_len = values[4]
        ilclass = values[8]
        genecount = int(values[9])
        fragment = values[10]
        if args.skip_fragments and fragment == 'True':
            continue

        if species not in breakdown:
            breakdown[species] = dict((col, list()) for col in outcols)
            pilocus_lengths[species] = list()

        if ilclass == 'iiLocus':
            if fragment == 'True':
                breakdown[species]['Fragment'].append(values)
            else:
                breakdown[species]['Intergenic'].append(values)
        elif ilclass == 'niLocus':
            breakdown[species]['ncRNA'].append(values)
        else:
            assert ilclass in ['piLocus', 'complex'], ilcid
            pilocus_lengths[species].append(int(values[3]))
            if ilclass == 'complex' or genecount > 1 or \
                    ilcid not in ilocus_class:
                breakdown[species]['Complex'].append(values)
            elif ilocus_class[ilcid] == 'Orphan':
                breakdown[species]['Orphan'].append(values)
            elif ilcid in hicons:
                breakdown[species]['Conserved'].append(values)
            else:
                breakdown[species]['Matched'].append(values)

    if args.table:
        locus2mrna = locus_mrna_map(root=args.rootdir)
        print(header.rstrip() + '\tClass\tmRNA')
        for spec in breakdown:
            for col in outcols:
                for ilocus in breakdown[spec][col]:
                    ilocus.append(col)
                    mrna = 'NA'
                    if ilocus[1] in locus2mrna:
                        mrna = locus2mrna[ilocus[1]]
                    ilocus.append(mrna)
                    print('\t'.join(ilocus))
        sys.exit(0)

    print('\t'.join(['Species'] + outcols))
    for species in sorted(breakdown):
        pilocus_lengths[species].sort()
        longpilocus = pilocus_lengths[species][-500]
        print(species, end='', sep='')
        for col in outcols:
            iloci = breakdown[species][col]
            if args.counts:
                print('\t%d' % len(iloci), end='', sep='')
            else:
                if args.skiplong and col in ['Conserved', 'Matched', 'Complex',
                                             'Orphan']:
                    cumlength = sum([int(x[4]) for x in iloci
                                     if int(x[3]) < 75000])
                else:
                    cumlength = sum([int(x[4]) for x in iloci])
                print('\t%d' % cumlength, end='', sep='')
        print('\n', end='')
