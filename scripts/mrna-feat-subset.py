#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import sys

desc = 'Extract feature info for hiLocus mRNA reps'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                    metavar='FILE', default=sys.stdout,
                    help='write results to specified file')
parser.add_argument('-s', metavar='int', type=int, default=3,
                    help='column in hiLocus file containing species label; '
                    'default is 3')
parser.add_argument('-m', metavar='int', type=int, default=5,
                    help='column in hiLocus file containing mRNA ID; default '
                    'is 5')
parser.add_argument('-S', metavar='int', type=int, default=1,
                    help='column in feature file containing species label; '
                    'default is 1')
parser.add_argument('-M', metavar='int', type=int, default=3,
                    help='column in feature file containing mRNA ID; default '
                    'is 3')
parser.add_argument('hiloci', type=argparse.FileType('r'),
                    default='data/hiloci-conserved.tsv',
                    help='hiLocus mRNA data table')
parser.add_argument('featfile', type=argparse.FileType('r'),
                    help='mRNA feature data table')
args = parser.parse_args()

mrnas2keep = dict()
next(args.hiloci)
for line in args.hiloci:
    values = line.split('\t')
    species = values[args.s - 1]
    mrnaid = values[args.m - 1]
    if species not in mrnas2keep:
        mrnas2keep[species] = dict()
    mrnas2keep[species][mrnaid] = True

print str(next(args.featfile)).rstrip()
for line in args.featfile:
    values = line.split('\t')
    species = values[args.S - 1]
    mrnaid = values[args.M - 1]
    if species in mrnas2keep and mrnaid in mrnas2keep[species]:
        print line.rstrip()
