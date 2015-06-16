#!/usr/bin/env python
#
# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import sys
import yaml
import ncbi

def get_args():
    desc = 'Execute the main HymHub build process'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-r', '--root', metavar='DIR', default='.',
                        help='HymHub root directory; default is current dir')
    parser.add_argument('--species', metavar='LIST', default=None,
                        help='comma-separated list of species labels to '
                        'process (such as "Amel,Hsal,Nvit,Pdom"); default is '
                        'to process all')
    parser.add_argument('-p', '--num_procs', metavar='N', default=1, type=int,
                        help='number of processors available for local tasks; '
                        'default is 1')
    parser.add_argument('-l', '--logfile', metavar='LOG', default=sys.stderr,
                        type=argparse.FileType('w'),
                        help='log file; default is terminal (stderr)')
    tasks = parser.add_argument_group('build tasks')
    tasks.add_argument('-d', '--download', action='store_true',
                       help='download data from remote servers')
    tasks.add_argument('-f', '--format', action='store_true',
                       help='polish raw primary data files')
    tasks.add_argument('-t', '--types', action='store_true',
                       help='extract data for various genomic feature types')
    tasks.add_argument('-s', '--stats', action='store_true',
                       help='compute statistics for each data type')
    tasks.add_argument('-c', '--cleanup', action='store_true',
                       help='clean up intermediate data files')
    return parser.parse_args()


def load_configs(species_list, rootdir='.'):
    configs = dict()
    for species in species_list:
        configfile = '%s/species/%s/data.yml' % (rootdir, species)
        with open(configfile, 'r') as cfg:
            configs[species] = yaml.load(cfg)
    return configs


def main(args=get_args()):
    if not args.download and not args.format and not args.types and \
            not args.stats and not args.cleanup:
        print >> sys.stderr, 'please specify build task(s)'
        sys.exit(1)

    if args.num_procs != 1:
        print >> sys.stderr, 'warning: parallel processing not yet supported'

    if args.species == None:
        args.species = ('Acep,Ador,Aech,Aflo,Amel,Bimp,Bter,Cflo,Dmel,Hsal,'
                        'Mrot,Nvit,Pbar,Pdom,Sinv,Tcas')
    args.species_list = args.species.split(',')
    configs = load_configs(args.species_list, args.root)

    if args.download:
        for species in args.species_list:
            dnasource = configs[species]['genomeseq']['source']
            assert dnasource in ['ncbi_scaffolds']
            if dnasource == 'ncbi_scaffolds':
                ncbi.download_scaffolds(configs[species], rootdir=args.root,
                                        logstream=args.logfile)

            annotsource = configs[species]['genomeannot']['source']
            assert annotsource in ['ncbi']
            if annotsource == 'ncbi':
                ncbi.download_annotation(configs[species], rootdir=args.root,
                                         logstream=args.logfile)

            proteinsource = configs[species]['proteinseq']['source']
            assert proteinsource in ['ncbi']
            if proteinsource == 'ncbi':
                ncbi.download_proteins(configs[species], rootdir=args.root,
                                       logstream=args.logfile)

    for species in args.species_list:
        pass


if __name__ == '__main__':
    main()
