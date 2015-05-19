#!/usr/bin/env python
import subprocess
"""
Compute a multiple sequence alignment for a hiLocus.
"""


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


def run_msa(proteinseqs, outfile=None, command='clustalo', path=None):
    """
    Align the specified protein sequences using clustalo.
    """

    program = command
    if path is not None:
        program = path + '/' + command
    args = [program, '--seqtype=Protein', '--infile=-', '--outfmt=clustal']
    if outfile is not None:
        args.append('--outfile=' + outfile)
    proc = subprocess.Popen(args, stdin=subprocess.PIPE)
    proc.communicate(input=proteinseqs)


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


if __name__ == '__main__':
    import argparse
    import sys

    desc = 'Align proteins corresponding to a hiLocus'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--cpath', default=None,
                        help='path to dir containing clustalw program (if not '
                        'in $PATH)')
    parser.add_argument('-p', '--path',
                        default='.', help='path to HymHub root directory')
    parser.add_argument('-o', '--out', default=None,
                        help='output file; default is terminal (stdout)')
    parser.add_argument(default=None, dest='hid',
                        help='ID of the hiLocus for which protein MSA will '
                        'be generated')

    args = parser.parse_args()

    hilocus = load_hilocus(args.hid, rootdir=args.path)
    iloci = hilocus[5].split(',')
    species = hilocus[6].split(',')

    protids = resolve_protein_ids(iloci, species, rootdir=args.path)
    proteinseqs = load_proteins(protids, species, rootdir=args.path)
    run_msa(proteinseqs, outfile=args.out, path=args.cpath)
