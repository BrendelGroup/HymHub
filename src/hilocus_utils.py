#!/usr/bin/env python
import subprocess


def parse_fasta(fp):
    """
    Stolen shamelessly from http://stackoverflow.com/a/7655072/459780.
    """
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name:
                yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name:
        yield (name, ''.join(seq))


def load_proteins(protids, specieslist, rootdir='.', suffix='rep-prot.fa'):
    """
    Load the specified protein sequences into memory.
    """

    proteinseqs = ''
    for species in specieslist:
        filename = '%s/species/%s/%s.%s' % (rootdir, species, species, suffix)
        for defline, seq in parse_fasta(open(filename, 'r')):
            pid = defline.split(' ')[0].split('|')[2]
            if pid in protids:
                proteinseqs += '%s\n%s\n' % (defline, seq)
    return proteinseqs


def resolve_protein_ids(ilocuslist, specieslist, rootdir='.',
                        suffix='protein2ilocus.txt'):
    """
    Determine the representative proteins corresponding to a list of iLoci.
    """

    protids = dict()
    for species in specieslist:
        filename = '%s/species/%s/%s.%s' % (rootdir, species, species, suffix)
        for line in open(filename, 'r'):
            proteinid, ilocusid = line.rstrip().split('\t')
            if ilocusid in ilocuslist:
                protids[proteinid] = 1
    return protids


def load_hilocus(hid, rootdir='.', filepath='data/hiloci.tsv'):
    """
    Given a hiLocus ID, search through the hiLocus data table to extract the
    relevant information.
    """
    filename = rootdir + '/' + filepath
    for line in open(filename, 'r'):
        values = line.rstrip().split()
        if values[0] == hid:
            return values

