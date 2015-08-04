#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import random
import sys
import hilocus_utils


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('Select hiLoci with single-copy orthologs from the main '
            'Hymenopteran lineages: bees, ants, vespid wasps, and parasitic '
            'wasps')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-m', '--multiple', action='store_true',
                        help='if all four lineages are represented in a '
                        'hiLocus but not in single copies, choose a '
                        'representative copy rather than discarding the '
                        'hiLocus')
    parser.add_argument('-s', '--seed', type=int, help='set seed for random '
                        'number generator')
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='hiLocus data table')
    args = parser.parse_args()

    if not args.seed:
        args.seed = random.randint(0, sys.maxint)
    random.seed(args.seed)
    print >> sys.stderr, 'Random seed: %d' % args.seed

    print '\t'.join(['ID', 'Ant', 'Bee', 'Vespid', 'Chalcid'])
    for line in args.hiloci:
        values = line.rstrip().split('\t')
        if values[4] not in ['Hymenoptera', 'Insects']:
            continue
        species = values[6].split(',')
        if 'Pdom' not in species or 'Nvit' not in species:
            continue
        iloci = values[5].split(',')
        hid = values[0]

        antspecies, antlocus = hilocus_utils.in_ants(iloci)
        beespecies, beelocus = hilocus_utils.in_bees(iloci)
        _, pdomlocus = hilocus_utils.in_pdom(iloci)
        _, nvitlocus = hilocus_utils.in_nvit(iloci)
        if None in [antlocus, beelocus, pdomlocus, nvitlocus]:
            # Lack representative from one or more clade; moving on
            continue

        print '\t'.join([hid, '%s:%s' % (antspecies, antlocus),
                         '%s:%s' % (beespecies, beelocus),
                         'Pdom:%s' % pdomlocus, 'Nvit:%s' % nvitlocus])
