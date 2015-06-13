#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.


def index_by_species(iloci):
    idx = dict()
    for locus in iloci:
        species = locus[6:10]
        if species not in idx:
            idx[species] = list()
        idx[species].append(locus)
    return idx


def in_clade(iloci, clade_list, require_single_copy=True):
    idx = index_by_species(iloci)
    for species in clade_list:
        if species in idx and len(idx[species]) == 1:
            return species, idx[species][0]

    if require_single_copy is not True:
        for species in clade_list:
            if species in idx:
                return species, idx[species][0]

    return None, None


def in_bees(iloci):
    return in_clade(iloci, ['Amel', 'Aflo', 'Bter', 'Bimp', 'Ador', 'Mrot'])


def in_ants(iloci):
    return in_clade(iloci, ['Acep', 'Aech', 'Hsal', 'Sinv', 'Cflo', 'Pbar'])


def in_nvit(iloci):
    return in_clade(iloci, ['Nvit'])


def in_pdom(iloci):
    return in_clade(iloci, ['Pdom'])


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
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='hiLocus data table')
    args = parser.parse_args()

    for line in args.hiloci:
        values = line.rstrip().split('\t')
        if values[4] not in ['Hymenoptera', 'Insects']:
            continue
        species = values[6].split(',')
        if 'Pdom' not in species or 'Nvit' not in species:
            continue
        iloci = values[5].split(',')

        antspecies, antlocus = in_ants(iloci)
        beespecies, beelocus = in_bees(iloci)
        _, pdomlocus = in_pdom(iloci)
        _, nvitlocus = in_nvit(iloci)
        if None in [antlocus, beelocus, pdomlocus, nvitlocus]:
            # Lack representative from one or more clade; moving on
            continue

        print '%s\t%s\t%s' % (antspecies, antlocus, values[0])
        print '%s\t%s\t%s' % (beespecies, beelocus, values[0])
        print 'Nvit\t%s\t%s' % (nvitlocus, values[0])
        print 'Pdom\t%s\t%s' % (pdomlocus, values[0])
