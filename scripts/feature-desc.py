#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
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
      if name: yield (name, ''.join(seq))
      name, seq = line, []
    else:
      seq.append(line)
  if name: yield (name, ''.join(seq))

def gc_content(dna):
  """
  Calculate the %GC content of a nucleotide sequence.
  """
  seqlength = len(dna)
    
  # Count A and T nucleotides, including the W ambiguity base representing
  # either A or T
  atcount = dna.count('A') + dna.count('a') + \
            dna.count('T') + dna.count('t') + \
            dna.count('W') + dna.count('w')

  # Count C and G nucleotides, including the S ambiguity base representing
  # either C or G
  gccount = dna.count('C') + dna.count('c') + \
            dna.count('G') + dna.count('g') + \
            dna.count('S') + dna.count('s')
  
  # Count all other ambiguous nucleotides; most will be Ns, but occasionally
  # there will be other IUPAC ambiguity symbols
  ncount = seqlength - atcount - gccount
  
  if atcount + gccount == 0:
      assert ncount == seqlength
      gccontent = 0.0
  else:
      gccontent = float(gccount) / float(gccount + atcount)
  return gccontent

def gc_skew(dna):
  """
  Calculate the GC skew of a nucleotide sequence: s = (G - C) / (G + C)
  """
  gcount = dna.count("G") + dna.count("g")
  ccount = dna.count("C") + dna.count("c")
  if gcount + ccount == 0:
    return 0.0
  return float(gcount - ccount) / float(gcount + ccount)

def ilocus_desc(gff3, fasta):
  """
  Given iLocus sequences and their corresponding annotations, generate a tabular
  record for each iLocus.
  """
  seqs = {}
  for defline, seq in parse_fasta(fasta):
    seqid = defline[1:].split(" ")[0]
    seqs[seqid] = seq

  for entry in gff3:
    if "\tlocus\t" not in entry:
      continue
    fields = entry.rstrip().split("\t")
    assert len(fields) == 9
    locusid = re.search("ID=([^;\n]+)", fields[8]).group(1)
    locuslen = int(fields[4]) - int(fields[3]) + 1
    locusseq = seqs[locusid]
    assert len(locusseq) == locuslen, "Locus '%s': length mismatch; gff=%d, fa=%d" % (locusid, locuslen, len(locusseq))
    gccontent = gc_content(locusseq)
    gcskew = gc_skew(locusseq)

    genecount = 0
    unannot = False
    if ";fragment=true" in entry:
      unannot = ";unannot=true" in entry
    elif ";gene=" in entry:
      locustype = "gene"
      gmatch = re.search(";gene=(\d+)", fields[8])
      assert gmatch
      genecount = int(gmatch.group(1))
    values = "%s %d %.3f %.3f %d %r" % (locusid, locuslen, gccontent, gcskew, genecount, unannot)
    yield values.split(" ")

if __name__ == "__main__":
  desc = "Calculate descriptive statistics of genomic features in tabluar form"
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument("--iloci", type=str, nargs=3,
                      metavar=("gff", "fa", "out"),
                      help="Compute iLocus statistics")
  args = parser.parse_args()

  # Process iLoci
  if args.iloci:
    a = args.iloci
    with open(a[0], "r") as gff, open(a[1], "r") as fa, open(a[2], "w") as out:
      header = "LocusId Length GCContent GCSkew GeneCount SeqUnannot".split(" ")
      print >> out, "\t".join(header)
      for fields in ilocus_desc(gff, fa):
        print >> out, "\t".join(fields)
