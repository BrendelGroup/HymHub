#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""
All of this would be much simpler if we could traverse each feature graph in a
manner similar to this.

    if feature.type == 'locus':
        for subfeature in feature:
            if subfeature.type == 'CDS':
                yield feature.get_attribute('ID'), \
                      subfeature.get_attribute('protein_id')
"""

import argparse
import sys
import re


def parse_ncbi(filehandle):
    """
    Parse iLocus / protein relationships from GFF3 files obtained from NCBI.

    In NCBI-derived GFF3 files, protein IDs are contained in the 'protein_id'
    attribute of CDS features. Therefore, to resolve the relationship between
    proteins and IDs, we must track CDS to mRNA, mRNA to gene, and gene to
    iLocus.
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
            if proteinid in proteins:
                if proteins[proteinid] != mrnaid:
                    print >> sys.stderr, 'duplicate protein %s' % proteinid
                pass
            else:
                geneid = mrna2gene[mrnaid]
                ilocusid = gene2loci[geneid]
                proteins[proteinid] = mrnaid
                yield proteinid, ilocusid


def parse_hymbase(filehandle):
    """
    Parse iLocus / protein relationships from HymenopteraBase GFF3 files.

    IDs of protein sequences are not present in HymenopteraBase-derived GFF3
    files, but they can be easily obtained from the corresponding mRNA IDs
    (changing an 'R' to a 'P'). To resolve the relationship between proteins
    and IDs, we must track mRNA to gene, and gene to iLocus.
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
            idmatch = re.search('Parent=([^;\n]+);.*Name=([^;\n]+)', fields[8])
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
