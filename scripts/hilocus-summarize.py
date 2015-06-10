#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
import sys


def in_clade(species, clade_list):
    for s in clade_list:
        if s in species:
            return s
    assert False


def in_bees(species):
    return in_clade(species, ['Amel', 'Aflo', 'Bter', 'Bimp', 'Ador', 'Mrot'])


def in_ants(species):
    return in_clade(species, ['Hsal', 'Sinv', 'Cflo'])


if __name__ == '__main__':
    for line in sys.stdin:
        values = line.rstrip().split('\t')
        if values[4] != 'Hymenoptera':
            continue
        species = values[6].split(',')
        if 'Pdom' not in species or 'Nvit' not in species:
            continue
        iloci = values[5].split(',')

        antrep = in_ants(species)
        beerep = in_bees(species)
        for locus in iloci:
            if antrep in locus:
                print '%s\t%s' % (antrep, locus)
            elif beerep in locus:
                print '%s\t%s' % (beerep, locus)
            elif 'Nvit' in locus:
                print 'Nvit\t%s' % locus
            elif 'Pdom' in locus:
                print 'Pdom\t%s' % locus
