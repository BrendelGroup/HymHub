#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import glob
from Bio import Phylo


def visit(clade, depth, depths, parents):
    """
    Recursive function to determine the depth and grouping of OTUs in the
    phylogeny.
    """
    for subclade in clade:
        if len(subclade) == 0:
            assert subclade.name in ['ant', 'bee', 'vespid', 'chalcid']
            depths[subclade.name] = depth
            parents[subclade.name] = clade
        else:
            visit(subclade, depth + 1, depths, parents)


def classify(depths, parents):
    """
    Determine which of the ants, bees, and vespid wasps are grouped most
    closely together from the given tree data.
    """
    for otu in ['ant', 'bee', 'vespid', 'chalcid']:
        assert otu in depths
        assert otu in parents
    if parents['ant'] == parents['bee'] == parents['vespid']:
        return 'AntBeePdom'
    elif parents['ant'] == parents['bee']:
        return 'AntBee'
    elif parents['ant'] == parents['vespid']:
        return 'AntPdom'
    elif parents['bee'] == parents['vespid']:
        return 'BeePdom'
    raise Exception('sanity check failed!')


def get_args():
    """Parse command-line arguments"""
    desc = 'Assess relationship of bees, ants, and wasps in gene trees'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-w', '--workdir', metavar='WD', default='.',
                        help='workdir (see hilocus-phylo.py); default is '
                        'current directory')
    return parser.parse_args()


def main(args=get_args()):
    pattern = '%s/*/outtree' % args.workdir
    files = glob.glob(pattern)
    for filename in files:
        tree = Phylo.parse(filename, 'newick').next()
        otu_depths = dict()
        otu_parents = dict()
        visit(tree.root, 1, otu_depths, otu_parents)
        cls = classify(otu_depths, otu_parents)
        print '%s\t%s' % (filename, cls)


if __name__ == '__main__':
    main()
