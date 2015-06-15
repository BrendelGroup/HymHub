#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.


if __name__ == '__main__':
    import argparse
    import sys
    import fasta_utils
    import hilocus_utils

    desc = 'Retrieve mRNA or protein sequences for each hiLocus quartet'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--cpath', default=None,
                        help='path to dir containing clustalo program (if not '
                        'in $PATH)')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-t', '--type', default='prot',
                        choices=['nucl', 'prot'],
                        help='sequence type; default is "prot"')
    parser.add_argument('-w', '--workdir', default='.',
                        help='working directory; default is .')
    parser.add_argument('qfile', type=argparse.FileType('r'),
                        help='quartet file (see hilocus-quartets.py); default '
                        'is stdin')

    args = parser.parse_args()
    if args.type == 'nucl':
        raise Exception('mRNA extraction not yet implemented')

    next(args.qfile)
    for line in args.qfile:
        hilocusid, ant, bee, pdom, nvit = line.rstrip().split('\t')
        species = list()
        iloci = list()
        for value in [ant, bee, pdom, nvit]:
            spec, ilocus = value.split(':')
            species.append(spec)
            iloci.append(ilocus)
        protids = hilocus_utils.resolve_protein_ids(iloci, species,
                                                    rootdir=args.path)
        outfilename = args.workdir + '/' + hilocusid + '.faa'
        with open(outfilename, 'w') as outfile:
            for defline, seq in hilocus_utils.retrieve_proteins(
                    protids, species, rootdir=args.path):
                print >> outfile, defline
                fasta_utils.format_seq(seq, outstream=outfile)
