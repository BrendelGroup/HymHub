#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.


if __name__ == '__main__':
    import argparse
    import sys
    import hilocus_utils

    desc = 'Prep data to infer phylogenies for hiLocus quartets'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--cpath', default=None,
                        help='path to dir containing clustalo program (if not '
                        'in $PATH)')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-w', '--workdir', default='.',
                        help='working directory; default is .')
    parser.add_argument('qfile', type=argparse.FileType('r'),
                        help='quartet file (see hilocus-quartets.py); default '
                        'is stdin')

    args = parser.parse_args()

    for line1 in args.qfile:
        line2 = next(args.qfile)
        line3 = next(args.qfile)
        line4 = next(args.qfile)
        species = list()
        iloci = list()
        hilocusid = None
        for line in [line1, line2, line3, line3]:
            spec, ilocus, hilocusid = line.rstrip().split('\t')
            species.append(spec)
            iloci.append(ilocus)
        protids = hilocus_utils.resolve_protein_ids(iloci, species,
                                                    rootdir=args.path)
        proteinseqs = hilocus_utils.load_proteins(protids, species,
                                                  rootdir=args.path)
        outfile = args.workdir + '/' + hilocusid + '.msa'
        hilocus_utils.run_msa(proteinseqs, outfile=outfile, outfmt='phylip',
                              path=args.cpath)
