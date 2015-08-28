#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.


if __name__ == '__main__':
    import argparse
    import glob
    import subprocess
    import sys
    import hilocus_utils

    desc = 'Use hiLocus protein quartets to infer gene phylogenies'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-d', '--debug', action='store_true', help='print '
                        'debugging messages')
    parser.add_argument('-j', '--jobs', type=int, default=1,
                        help='number of concurrent processes to run while '
                        'performing multiple sequence alignment and phylogeny '
                        'inference; default is 1')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-w', '--workdir', default='.',
                        help='working directory; default is .')
    parser.add_argument('-s', '--skip-prep', action='store_true',
                        help='Skip the prep step')
    parser.add_argument('qfile', type=argparse.FileType('r'),
                        help='quartet file (see hilocus-quartets.py); default '
                        'is stdin')

    args = parser.parse_args()
    if not args.skip_prep:
        hilocus_utils.prep_phylo(args.workdir, args.qfile, rootdir=args.path)
    if args.debug:
        print >> sys.stderr, 'prep_phylo done!'
    phyloscript = args.path + '/scripts/msa-phylo.sh'
    dirs = glob.glob(args.workdir + '/*')
    cmdargs = ['parallel', '--gnu', '--jobs', str(args.jobs), phyloscript,
               '{}', ':::']
    cmdargs.extend(dirs)
    subprocess.call(cmdargs)
