#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import sys
import re


def parse_ncbi(filehandle):
    """
    """
    gene2loci = dict()
    mrna2gene = dict()
    proteins = dict()
    for line in filehandle:
        fields = line.split("\t")
        if len(fields) != 9:
            continue
        feattype = fields[2]
        if feattype == 'gene':
            idmatch = re.search('ID=([^;\n]+);Parent=([^;\n]+)', fields[8])
            assert idmatch, \
                'Unable to parse gene and iLocus IDs: %s' % fields[8]
            geneid = idmatch.group(1)
            ilocusid = idmatch.group(2)
            gene2loci[geneid] = ilocusid
        elif feattype == 'mRNA':
            idmatch = re.search('ID=([^;\n]+);Parent=([^;\n]+)', fields[8])
            assert idmatch, \
                'Unable to parse mRNA and gene IDs: %s' % fields[8]
            mrnaid = idmatch.group(1)
            geneid = idmatch.group(2)
            mrna2gene[mrnaid] = geneid
        elif feattype == 'CDS':
            idmatch = re.search('Parent=([^;\n]+).*protein_id=([^;\n]+)',
                                fields[8])
            assert idmatch, \
                'Unable to parse protein and mRNA IDs: %s' % fields[8]
            mrnaid = idmatch.group(1)
            proteinid = idmatch.group(2)
            if proteinid not in proteins:
                geneid = mrna2gene[mrnaid]
                ilocusid = gene2loci[geneid]
                proteins[proteinid] = 1
                yield proteinid, ilocusid


def parse_hymbase(filehandle):
    """
    """
    gene2loci = dict()
    for line in filehandle:
        fields = line.split("\t")
        if len(fields) != 9:
            continue
        feattype = fields[2]
        if feattype == 'gene':
            idmatch = re.search('ID=([^;\n]+);Parent=([^;\n]+)', fields[8])
            assert idmatch, \
                'Unable to parse gene and iLocus IDs: %s' % fields[8]
            geneid = idmatch.group(1)
            ilocusid = idmatch.group(2)
            gene2loci[geneid] = ilocusid
        elif feattype == 'mRNA':
            idmatch = re.search('Parent=([^;\n]+);Name=([^;\n]+)', fields[8])
            assert idmatch, \
                'Unable to parse mRNA and gene IDs: %s' % fields[8]
            mrnaid = idmatch.group(2)
            geneid = idmatch.group(1)
            locusid = gene2loci[geneid]
            proteinid = re.sub('-R', '-P', mrnaid)
            yield proteinid, locusid


if __name__ == '__main__':
    desc = 'Parse protein --> iLocus mapping from an iLocus GFF3 file'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--mode', type=str, default='ncbi',
                        help='Mode (ncbi or hymbase)')
    parser.add_argument('gff3', type=argparse.FileType('r'),
                        help='iLocus GFF3 file')
    args = parser.parse_args()

    parse_func = parse_ncbi
    if args.mode == 'hymbase':
        parse_func = parse_hymbase
    for pid, lid in parse_func(args.gff3):
        print "%s\t%s" % (pid, lid)
