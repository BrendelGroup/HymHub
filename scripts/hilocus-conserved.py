#!/usr/bin/env python
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import sys
import hilocus_utils
import hym_species


def ilocus_isoforms(rootdir='.'):
    """
    Determine the mapping of iLocus IDs to mRNA and protein IDs.

    Given the HymHub root directory, mine the relevant data files for mappings
    of iLocus IDs to mRNA and protein IDs. Create and return a dictionary with
    iLocus IDs as keys and tuples of mRNA IDs and protein IDs as values.
    """
    ilocus2mrna = dict()
    mapping = dict()
    for species in hym_species.labels:
        mrnafile = '%s/species/%s/%s.ilocus.mrnas.txt' % (rootdir, species,
                                                          species)
        protfile = '%s/species/%s/%s.protein2ilocus.txt' % (rootdir, species,
                                                            species)
        with open(mrnafile, 'r') as fhm, open(protfile, 'r') as fhp:
            for line in fhm:
                hid, mid = line.rstrip().split()
                ilocus2mrna[hid] = mid
            for line in fhp:
                pid, hid = line.rstrip().split()
                mid = ilocus2mrna[hid]
                mapping[hid] = (mid, pid)

    return mapping


if __name__ == '__main__':
    import argparse
    import sys

    desc = ('Select conserved hiLoci based on the specified criteria')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-m', '--mode', default='rep', help='specify the '
                        '"mode" used to query conservation; "rep" selects '
                        'hiLoci with at least one single-copy ortholog in each'
                        ' of the 4 primary lineages; "six" selects hiLoci with'
                        ' single-copy orthologs in Amel, Bter, Hsal, Cflo, '
                        'Pdom, and Nvit; "four" selects hiLoci with single-'
                        'copy orthologs in Amel, Hsal, Pdom, and Nvit; a '
                        'comma-separated list of species labels will select '
                        'hiLoci with single-copy orthologs in those species; '
                        'default is "rep"')
    parser.add_argument('-r', '--rootdir', default='.', metavar='RD',
                        help='path to HymHub root directory; default is '
                        'current directory')
    parser.add_argument('hiloci', type=argparse.FileType('r'),
                        default=sys.stdin, help='hiLocus data table')
    args = parser.parse_args()

    if args.mode not in ['rep', 'six', 'four']:
        speclabs = args.mode.split(',')
        for speclab in speclabs:
            assert speclab in hym_species.labels, \
                'Invalid species label %s' % speclab

    ilocus_mapping = ilocus_isoforms(rootdir=args.rootdir)
    simple = hilocus_utils.load_simple_iloci(args.rootdir)

    print '\t'.join(['hiLocus', 'iLocus', 'Species', 'Lineage', 'Mrna',
                     'Protein'])
    for line in args.hiloci:
        values = line.rstrip().split('\t')
        species = values[6].split(',')
        iloci = values[5].split(',')
        hid = values[0]

        if args.mode in ['rep', 'six', 'four']:
            if values[4] not in ['Hymenoptera', 'Insects']:
                continue
            if 'Pdom' not in species or 'Nvit' not in species:
                continue

        if args.mode == 'rep':
            ants = hilocus_utils.in_ants(iloci, as_list=True,
                                         simple_iloci=simple)
            bees = hilocus_utils.in_bees(iloci, as_list=True,
                                         simple_iloci=simple)
            pdom = hilocus_utils.in_pdom(iloci, as_list=True,
                                         simple_iloci=simple)
            nvit = hilocus_utils.in_nvit(iloci, as_list=True,
                                         simple_iloci=simple)
            if None in [ants, bees, pdom, nvit]:
                # Lack representative from one or more clades; moving on
                continue
            scos = ants + bees + pdom + nvit

        elif args.mode == 'six' or args.mode == 'four':
            if args.mode == 'six':
                queryfunc = hilocus_utils.in_six
                testlen = 6
            elif args.mode == 'four':
                queryfunc = hilocus_utils.in_four
                testlen = 4
            scos = queryfunc(iloci, as_list=True, simple_iloci=simple)
            if scos is None or len(scos) != testlen:
                # Lack representative from one or more clades; moving on
                continue

        else:
            scos = hilocus_utils.in_clade(iloci, speclabs, as_list=True,
                                          simple_iloci=simple)
            if scos is None or len(scos) != len(speclabs):
                # Lack representative from one or more clades; moving on
                continue

        for spec, ilocus, lineage in scos:
            mrnaid, protid = ilocus_mapping[ilocus]
            print '\t'.join([hid, ilocus, spec, lineage, mrnaid, protid])
