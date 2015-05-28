#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import sys


def parse_fasta(data):
    """
    Load sequences in Fasta format.

    This generator function yields a tuple containing a defline and a sequence
    for each record in the Fasta data. Stolen shamelessly from
    http://stackoverflow.com/a/7655072/459780.
    """
    name, seq = None, []
    for line in data:
        line = line.rstrip()
        if line.startswith('>'):
            if name:
                yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name:
        yield (name, ''.join(seq))


def format_seq(seq, linewidth=80, outstream=sys.stdout):
    """Print a sequence in a readable format."""
    if linewidth == 0 or len(seq) <= linewidth:
        print >> outstream, seq
        return

    i = 0
    while i < len(seq):
        print >> outstream, seq[i:i+linewidth]
        i += linewidth


def test_format_seq():
    """[fasta_utils] Test sequence formatting"""
    import StringIO

    seq = ('TCTCCCTCCA'
           'ACGCCCGAAC'
           'GTGTCTGCTC'
           'ATTTCAAGCA'
           'CACGCATGAA'
           'CGGCATCGCG'
           'CAGACGTGCG'
           'AGCGAGCGCA')

    sio = StringIO.StringIO()
    format_seq(seq, linewidth=0, outstream=sio)
    assert sio.getvalue() == seq + '\n'
    sio.close()

    sio = StringIO.StringIO()
    format_seq(seq, linewidth=40, outstream=sio)
    assert sio.getvalue() == ('TCTCCCTCCA'
                              'ACGCCCGAAC'
                              'GTGTCTGCTC'
                              'ATTTCAAGCA\n'
                              'CACGCATGAA'
                              'CGGCATCGCG'
                              'CAGACGTGCG'
                              'AGCGAGCGCA\n')
    sio.close()

    sio = StringIO.StringIO()
    format_seq(seq, linewidth=20, outstream=sio)
    assert sio.getvalue() == ('TCTCCCTCCA'
                              'ACGCCCGAAC\n'
                              'GTGTCTGCTC'
                              'ATTTCAAGCA\n'
                              'CACGCATGAA'
                              'CGGCATCGCG\n'
                              'CAGACGTGCG'
                              'AGCGAGCGCA\n')
    sio.close()
