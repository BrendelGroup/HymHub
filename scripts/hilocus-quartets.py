#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import random
import sys


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('For each hiLocus conserved in the four main hymenopteran '
            'lineages, select a representative quartet of iLoci (one per '
            'lineage)')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', '--seed', type=int, help='set seed for random '
                        'number generator')
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='conserved hiLocus table')
    args = parser.parse_args()

    if not args.seed:
        args.seed = random.randint(0, sys.maxint)
    random.seed(args.seed)
    print >> sys.stderr, 'Random seed: %d' % args.seed

    print '\t'.join(['ID', 'Ant', 'Bee', 'Vespid', 'Chalcid'])

    next(args.hiloci)
    iloci = dict()
    for line in args.hiloci:
        hid, iid, species, lineage, mrna, protein = line.split()
        if hid not in iloci:
            iloci[hid] = dict()
        if lineage not in iloci[hid]:
            iloci[hid][lineage] = list()
        iloci[hid][lineage].append((species, iid))

    for hid in sorted(iloci):
        values = [hid]
        for lineage in ['Ants', 'Bees', 'Pdom', 'Nvit']:
            random.shuffle(iloci[hid][lineage])
            values.append('%s:%s' % (iloci[hid][lineage][0]))
        print '\t'.join(values)
