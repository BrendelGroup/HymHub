#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import hilocus_utils


def iloci_for_species(spec, phyloclass=None, ilocus_count_filter=None,
                      rootdir='.', filepath='data/hiloci.tsv'):
    assert spec in ['Ador', 'Aflo', 'Amel', 'Bimp', 'Bter', 'Cflo', 'Dmel',
                    'Hsal', 'Mrot', 'Nvit', 'Pdom', 'Sinv', 'Tcas']

    hilocus_filename = rootdir + '/' + filepath
    with open(hilocus_filename) as infile:
        next(infile)
        for line in infile:
            fields = line.rstrip().split('\t')
            hilocus_species = fields[6].split(',')
            if spec not in hilocus_species:
                continue
            if phyloclass is not None:
                if isinstance(phyloclass, str):
                    if fields[4] != phyloclass:
                        continue
                else:
                    if fields[4] not in phyloclass:
                        continue
            if ilocus_count_filter is not None:
                count = int(fields[2])
                if isinstance(ilocus_count_filter, tuple):
                    if count < ilocus_count_filter[0] or \
                       count > ilocus_count_filter[1]:
                        continue
                else:
                    if count != ilocus_count_filter:
                        continue
            iloci = fields[5].split(',')
            for ilocus in iloci:
                if ilocus.startswith('HymHub' + spec):
                    yield ilocus

if __name__ == '__main__':
    import argparse

    desc = 'Retrieve hiLocus-related proteins meeting the specified criteria'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--phyloclass', default=None,
                        help='filter hiLoci by phylogenetic classification')
    parser.add_argument('-c', '--locuscount', default=None,
                        help='filter hiLoci by iLocus count; can be a single '
                        'integer value to be matched (such as "11") or a '
                        'comma-separated pair of integers representing a '
                        'closed interval (such as "8,10")')
    parser.add_argument('species', help='retrieve proteins from this species '
                        '(provide 4-letter species abbreviation such as "Amel"'
                        'or "Pdom")')
    args = parser.parse_args()

    if ',' in args.locuscount:
        lc_filter = [int(x) for x in args.locuscount.split(',')]
    else:
        lc_filter = int(args.locuscount)
    iloci = list(iloci_for_species(args.species, phyloclass=args.phyloclass,
                                   ilocus_count_filter=lc_filter))
    protein_ids = hilocus_utils.resolve_protein_ids(iloci, [args.species])
    print hilocus_utils.load_proteins(protein_ids, [args.species])
