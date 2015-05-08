#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import re
import sys


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


def format_seq(seq, length=80, outstream=sys.stdout):
    if len(seq) <= length:
        print >> outstream, seq
        return

    i = 0
    while i < len(seq):
        print >> outstream, seq[i:i+length]
        i += length


if __name__ == '__main__':
    usage = 'python %s seqidlist.txt seqs.fasta' % sys.argv[0]
    assert len(sys.argv) == 3, 'Usage: %s' % usage
    seqlist = sys.argv[1]
    seqfile = sys.argv[2]

    ids = dict()
    with open(seqlist, 'r') as fp:
        for line in fp:
            seqid = line.rstrip()
            ids[seqid] = 1

    with open(seqfile, 'r') as fp:
        for defline, seq in parse_fasta(fp):
            seqid = re.search('>(\S+)', defline).group(1)
            if seqid in ids:
                print defline
                format_seq(seq)
