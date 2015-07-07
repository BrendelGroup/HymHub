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


def in_clade(iloci, clade_list):
    idx = index_by_species(iloci)
    count = 0
    for species in clade_list:
        if species in idx and len(idx[species]) == 1:
            count += 1
    return count


def in_bees(iloci):
    return in_clade(iloci, ['Amel', 'Aflo', 'Bter', 'Bimp', 'Ador', 'Mrot'])


def in_ants(iloci):
    return in_clade(iloci, ['Acep', 'Aech', 'Hsal', 'Sinv', 'Cflo', 'Pbar'])


def in_nvit(iloci):
    return in_clade(iloci, ['Nvit'])


def in_pdom(iloci):
    return in_clade(iloci, ['Pdom'])


def in_dmel(iloci):
    return in_clade(iloci, ['Dmel'])


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('Select hiLoci with single-copy orthologs from Pdom, Nvit, '
            'multiple ants, multiple bees, and Dmel ')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='hiLocus data table')
    args = parser.parse_args()

    for line in args.hiloci:
        values = line.rstrip().split('\t')
        if values[4] not in ['Hymenoptera', 'Insects']:
            continue
        iloci = values[5].split(',')
        hid = values[0]

        antcount = in_ants(iloci)
        beecount = in_bees(iloci)
        pdomcount = in_pdom(iloci)
        nvitcount = in_nvit(iloci)
        dmelcount = in_dmel(iloci)
        if antcount > 1 and beecount > 1 and pdomcount == 1 and \
                nvitcount == 1 and dmelcount == 1:
            print hid
