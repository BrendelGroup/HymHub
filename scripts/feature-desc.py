#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import argparse
import re
import sys
import fasta_utils


def gc_content(dna):
    """Calculate the %GC content of a nucleotide sequence."""
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
    Calculate the GC skew of a nucleotide sequence.

    s = (G - C) / (G + C)
    """
    gcount = dna.count("G") + dna.count("g")
    ccount = dna.count("C") + dna.count("c")
    if gcount + ccount == 0:
        return 0.0
    return float(gcount - ccount) / float(gcount + ccount)


def n_content(dna):
    """Calculate the proportion of ambigious nucleotides in a DNA sequence."""
    ncount = dna.count("N") + dna.count("n") + \
        dna.count("X") + dna.count("x")
    if ncount == 0:
        return 0.0
    return float(ncount) / float(len(dna))


def ilocus_classify(ilocus):
    """Determine the type of gene(s), if any, encoded in this iLocus."""
    fields = ilocus.split("\t")
    assert len(fields) == 9
    attrs = fields[8]

    counts = {}
    for keyvaluepair in attrs.split(";"):
        key, value = keyvaluepair.split("=")
        if key not in ["ID", "fragment", "unannot", "merged", "gene",
                       "left_overlap", "right_overlap", "intron_gene"]:
            counts[key] = 1

    if "intron_gene" in attrs:
        return "intron_gene"

    if len(counts) == 0:
        return "geneless"

    if len(counts) > 1:
        assert "geneless" not in counts
        return "mixed"

    rnatype = counts.keys()[0]
    if rnatype in ["transcript", "primary_transcript"]:
        rnatype = "ncRNA"
    return rnatype


def ilocus_desc(gff3, fasta):
    """
    Generate a tabular record for each iLocus in the input.

    - gff3: file handle to a GFF3 file containing iLocus annotations
    - fasta: file handle to a Fasta file containing iLocus sequences
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        seqid = defline[1:].split(" ")[0]
        assert seqid not in seqs
        seqs[seqid] = seq

    for entry in gff3:
        if "\tlocus\t" not in entry:
            continue
        fields = entry.rstrip().split("\t")
        assert len(fields) == 9
        locuspos = "%s_%s-%s" % (fields[0], fields[3], fields[4])
        locusid = locuspos
        locusidmatch = re.search("ID=([^;\n]+)", fields[8])
        if locusidmatch:
            locusid = locusidmatch.group(1)
        locuslen = int(fields[4]) - int(fields[3]) + 1
        locusseq = seqs[locusid]
        assert len(locusseq) == locuslen, \
            "Locus '%s': length mismatch; gff=%d, fa=%d" % (
            locusid, locuslen, len(locusseq))
        gccontent = gc_content(locusseq)
        gcskew = gc_skew(locusseq)
        ncontent = n_content(locusseq)
        left_overlap = 0
        lomatch = re.search("left_overlap=(\d+)", fields[8])
        if lomatch:
            left_overlap = int(lomatch.group(1))
        right_overlap = 0
        romatch = re.search("right_overlap=(\d+)", fields[8])
        if romatch:
            right_overlap = int(romatch.group(1))

        locusclass = ilocus_classify(entry.rstrip())
        genecount = 0
        attrs = fields[8]
        fragment = "fragment=true" in attrs
        unannot = "unannot=true" in attrs
        if "gene=" in attrs:
            locustype = "gene"
            gmatch = re.search("gene=(\d+)", attrs)
            assert gmatch
            genecount = int(gmatch.group(1))
        values = "%s %s %d %.3f %.3f %.3f %s %d %r %r %d %d" % (
            locusid, locuspos, locuslen, gccontent, gcskew, ncontent,
            locusclass, genecount, fragment, unannot, left_overlap,
            right_overlap)
        yield values.split(" ")


def premrna_desc(gff3, fasta):
    """
    Given pre-mRNA sequences and corresponding annotations, generate a tabular
    record for each.
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        seqid = defline[1:].split(" ")[0]
        assert seqid not in seqs
        seqs[seqid] = seq

    mrnaid = ""
    mrnaacc = ""
    mrnalen = 0
    gccontent = 0.0
    gcskew = 0.0
    ncontent = 0.0
    exoncount = 0
    introncount = 0
    utr5plen = 0
    utr3plen = 0
    for entry in gff3:
        if "\tmRNA\t" in entry:
            fields = entry.rstrip().split("\t")
            assert len(fields) == 9
            mrnaid = re.search("ID=([^;\n]+)", fields[8]).group(1)
            mrnaacc = re.search("Name=([^;\n]+)", fields[8]).group(1)
            mrnalen = int(fields[4]) - int(fields[3]) + 1
            mrnaseq = seqs[mrnaid]
            assert len(mrnaseq) == mrnalen, \
                "mRNA '%s': length mismatch; gff=%d, fa=%d" % (
                mrnaid, mrnalen, len(mrnaseq))
            gccontent = gc_content(mrnaseq)
            gcskew = gc_skew(mrnaseq)
            ncontent = n_content(mrnaseq)
        elif "\texon\t" in entry:
            exoncount += 1
        elif "\tintron\t" in entry:
            introncount += 1
        elif "\tfive_prime_UTR\t" in entry:
            fields = entry.rstrip().split("\t")
            assert len(fields) == 9
            utr5plen += int(fields[4]) - int(fields[3]) + 1
        elif "\tthree_prime_UTR\t" in entry:
            fields = entry.rstrip().split("\t")
            assert len(fields) == 9
            utr3plen += int(fields[4]) - int(fields[3]) + 1
        elif "###" in entry:
            values = "%s %s %d %.3f %.3f %.3f %d %d %d %d" % (
                mrnaid, mrnaacc, mrnalen, gccontent, gcskew, ncontent,
                exoncount, introncount, utr5plen, utr3plen)
            mrnaid = ""
            mrnaacc = ""
            mrnalen = 0
            gccontent = 0.0
            gcskew = 0.0
            ncontent = 0.0
            exoncount = 0
            exonlen = 0
            introncount = 0
            utr5plen = 0
            utr3plen = 0
            yield values.split(" ")


def mrna_desc(gff3, fasta):
    """
    Given mature (sans introns) mRNA sequences and their corresponding
    annotations, generate a tabular record for each mRNA.
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        seqid = defline[1:].split(" ")[0]
        assert seqid not in seqs
        seqs[seqid] = seq

    mrnaid = ""
    mrnaacc = ""
    mrnalen = 0
    for entry in gff3:
        if "\tmRNA\t" in entry:
            fields = entry.rstrip().split("\t")
            assert len(fields) == 9
            mrnaid = re.search("ID=([^;\n]+)", fields[8]).group(1)
            mrnalen += int(fields[4]) - int(fields[3]) + 1
            mrnaacc = re.search("Name=([^;\n]+)", fields[8]).group(1)
        elif "###" in entry:
            mrnaseq = seqs[mrnaid]
            assert len(mrnaseq) == mrnalen, \
                "mature mRNA '%s': length mismatch; gff=%d, fa=%d" % (
                mrnaid, mrnalen, len(mrnaseq))
            gccontent = gc_content(mrnaseq)
            gcskew = gc_skew(mrnaseq)
            ncontent = n_content(mrnaseq)
            values = "%s %s %d %.3f %.3f %.3f" % (
                mrnaid, mrnaacc, mrnalen, gccontent, gcskew, ncontent)
            mrnaid = ""
            mrnaacc = ""
            mrnalen = 0
            yield values.split(" ")


def cds_desc(gff3, fasta):
    """
    Given CDS sequences and their corresponding annotations, generate a tabular
    record for each CDS.
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        seqid = defline[1:].split(" ")[0]
        assert seqid not in seqs
        seqs[seqid] = seq

    cdsid = ""
    cdslen = 0
    for entry in gff3:
        if "\tCDS\t" in entry:
            fields = entry.rstrip().split("\t")
            assert len(fields) == 9
            parentid = re.search("Parent=([^;\n]+)", fields[8]).group(1)
            cdsmatch = re.search("ID=([^;\n]+)", fields[8])
            if cdsmatch:
                cdsid = cdsmatch.group(1)
            else:
                cdsid = parentid
            cdslen += int(fields[4]) - int(fields[3]) + 1
        elif "###" in entry:
            cdsseq = seqs[cdsid]
            assert len(cdsseq) == cdslen, \
                "CDS '%s': length mismatch; gff=%d, fa=%d" % (
                cdsid, cdslen, len(cdsseq))
            gccontent = gc_content(cdsseq)
            gcskew = gc_skew(cdsseq)
            ncontent = n_content(cdsseq)
            values = "%s %s %d %.3f %.3f %.3f" % (
                cdsid, parentid, cdslen, gccontent, gcskew, ncontent)
            cdsid = ""
            cdslen = 0
            yield values.split(" ")


def feat_overlap(f1, f2):
    """
    Given two features (lists of length=9 from GFF3), determine whether they
    overlap.
    """
    f1start = int(f1[3])
    f1end = int(f1[4])
    f2start = int(f2[3])
    f2end = int(f2[4])

    if f1start <= f2end and f1end >= f2start:
        return True
    return False


def exon_context(exon, start, stop):
    """
    Given an exon, a start codon, and a stop codon (GFF3 entries),
    determine the context of the exon:
      - cds (entirely coding)
      - 5putr (entirely 5' UTR)
      - 3putr (entirely 3' UTR)
      - start (includes start codon)
      - stop (includes stop codon)
      - complete (includes both start and stop codon)
    """
    assert start and stop
    exon = exon.split("\t")
    start = start.split("\t")
    stop = stop.split("\t")
    assert len(exon) == 9 and len(start) == 9 and len(stop) == 9

    hasstart = feat_overlap(exon, start)
    hasstop = feat_overlap(exon, stop)
    if hasstart or hasstop:
        if hasstart and hasstop:
            return "complete"
        elif hasstart:
            return "start"
        else:
            assert hasstop
            return "stop"

    exonstart = int(exon[3])
    exonend = int(exon[4])
    codonnucs = [start[3], start[4], stop[3], stop[4]]
    codonnucs = [int(x) for x in codonnucs]
    leftmostnuc = min(codonnucs)
    rightmostnuc = max(codonnucs)
    if exonend < leftmostnuc:
        if exon[6] == "-":
            return "3putr"
        else:
            return "5putr"
    elif exonstart > rightmostnuc:
        if exon[6] == "-":
            return "5putr"
        else:
            return "3putr"
    else:
        assert exonstart > leftmostnuc and exonend < rightmostnuc
        return "cds"


def exon_desc(gff3, fasta):
    """
    Given exon sequences and their corresponding annotations, generate a
    tabular record for each exon.
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        exonpos = defline[1:].split(" ")[1]
        seqs[exonpos] = seq

    reported_exons = {}
    exons, cdss = [], {}
    start, stop = None, None
    for entry in gff3:
        if "\texon\t" in entry:
            exons.append(entry)
        elif "\tCDS\t" in entry:
            fields = entry.split("\t")
            pos = "%s_%s-%s%s" % (fields[0], fields[3], fields[4], fields[6])
            cdss[pos] = entry
        elif "\tstart_codon\t" in entry:
            start = entry
        elif "\tstop_codon\t" in entry:
            stop = entry
        elif "###" in entry:
            xcept = False
            for exonpos in cdss:
                if ";exception=ribosomal slippage" in cdss[exonpos]:
                    xcept = True
            if xcept:
                exons, cdss = [], {}
                start, stop = None, None
                continue
            assert start, "No start codon for exon(s): %s" % exons[0]
            assert stop,  "No stop codon for exon(s): %s" % exons[0]
            for exon in exons:
                fields = exon.split("\t")
                assert len(
                    fields) == 9, "entry does not have 9 fields: %s" % exon
                mrnaid = re.search("Parent=([^;\n]+)", fields[8]).group(1)
                exonpos = "%s_%s-%s%s" % (fields[0],
                                          fields[3], fields[4], fields[6])
                if exonpos in reported_exons:
                    continue
                exonlength = int(fields[4]) - int(fields[3]) + 1
                exonseq = seqs[exonpos]
                assert len(exonseq) == exonlength, \
                    "exon '%s': length mismatch; gff=%d, fa=%d" % (
                    exonpos, exonlength, len(exonseq))
                gccontent = gc_content(exonseq)
                gcskew = gc_skew(exonseq)
                ncontent = n_content(exonseq)
                context = exon_context(exon, start, stop)
                phase = None
                remainder = None
                if context == "cds":
                    cexon = cdss[exonpos]
                    phase = int(cexon.split("\t")[7])
                    remainder = (exonlength - phase) % 3
                values = "%s %s %d %.3f %.3f %.3f %s %r %r" % (
                    exonpos, mrnaid, exonlength, gccontent, gcskew, ncontent,
                    context, phase, remainder)
                reported_exons[exonpos] = 1
                yield values.split(" ")
            exons, cdss = [], {}
            start, stop = None, None


def intron_context(intron, start, stop):
    """
    Given an intron, a start codon, and a stop codon (GFF3 entries),
    determine the context of the exon:
      - cds (entirely coding)
      - 5putr (entirely 5' UTR)
      - 3putr (entirely 3' UTR)
      - start (includes start codon)
      - stop (includes stop codon)
      - complete (includes both start and stop codon)
    """
    assert start and stop
    intron = intron.split("\t")
    start = start.split("\t")
    stop = stop.split("\t")
    assert len(intron) == 9 and len(start) == 9 and len(stop) == 9

    intronstart = int(intron[3])
    intronend = int(intron[4])
    codonnucs = [start[3], start[4], stop[3], stop[4]]
    codonnucs = [int(x) for x in codonnucs]
    leftmostnuc = min(codonnucs)
    rightmostnuc = max(codonnucs)
    if intronend < leftmostnuc:
        if intron[6] == "-":
            return "3putr"
        else:
            return "5putr"
    elif intronstart > rightmostnuc:
        if intron[6] == "-":
            return "5putr"
        else:
            return "3putr"
    else:
        assert intronstart > leftmostnuc and intronend < rightmostnuc
        return "cds"


def intron_desc(gff3, fasta):
    """
    Given intron sequences and their corresponding annotations, generate a
    tabular record for each intron.
    """
    seqs = {}
    for defline, seq in fasta_utils.parse_fasta(fasta):
        intronpos = defline[1:].split(" ")[1]
        seqs[intronpos] = seq

    reported_introns = {}
    introns = []
    start, stop = None, None
    for entry in gff3:
        if "\tintron\t" in entry:
            introns.append(entry)
        elif "\tstart_codon\t" in entry:
            start = entry
        elif "\tstop_codon\t" in entry:
            stop = entry
        elif "###" in entry:
            assert start, "No start codon for introns(s): %s" % introns[0]
            assert stop,  "No stop codon for introns(s): %s" % introns[0]
            if len(introns) > 0:
                for intron in introns:
                    fields = intron.split("\t")
                    assert len(fields) == 9, \
                        "entry does not have 9 fields: %s" % intron
                    mrnaid = re.search("Parent=([^;\n]+)", fields[8]).group(1)
                    intronpos = "%s_%s-%s%s" % (fields[0], fields[3],
                                                fields[4], fields[6])
                    if intronpos in reported_introns:
                        continue
                    intronlength = int(fields[4]) - int(fields[3]) + 1
                    intronseq = seqs[intronpos]
                    assert len(intronseq) == intronlength, \
                        "intron '%s': length mismatch; gff=%d, fa=%d" % (
                            intronpos, intronlength, len(intronseq))
                    gccontent = gc_content(intronseq)
                    gcskew = gc_skew(intronseq)
                    ncontent = n_content(intronseq)
                    context = intron_context(intron, start, stop)
                    values = "%s %s %d %.3f %.3f %.3f %s" % (
                        intronpos, mrnaid, intronlength, gccontent, gcskew,
                        ncontent, context)
                    reported_introns[intronpos] = 1
                    yield values.split(" ")
            introns = []
            start, stop = None, None
            continue

if __name__ == "__main__":
    desc = "Calculate descriptive statistics of genome features"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--species", type=str, default="default",
                        metavar="Spec", help="specify species label")
    parser.add_argument("--iloci", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute iLocus statistics")
    parser.add_argument("--prnas", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute stats on pre-mRNAs")
    parser.add_argument("--mrnas", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute stats on mature mRNAs")
    parser.add_argument("--cds", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute CDS statistics")
    parser.add_argument("--exons", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute exon statistics")
    parser.add_argument("--introns", type=str, nargs=3,
                        metavar=("gff", "fa", "out"),
                        help="compute intron statistics")
    args = parser.parse_args()

    # Process iLoci
    if args.iloci:
        a = args.iloci
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa,  \
                open(a[2], "w") as out:
            header = ["Species", "LocusId", "LocusPos", "Length", "GCContent",
                      "GCSkew", "NContent", "LocusClass", "GeneCount",
                      "Fragment", "SeqUnannot", "LeftOverlap", "RightOverlap"]
            print >> out, "\t".join(header)
            for fields in ilocus_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)

    # Process pre-mRNAs
    if args.prnas:
        a = args.prnas
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa,  \
                open(a[2], "w") as out:
            header = ["Species", "MrnaId", "Accession", "Length", "GCContent",
                      "GCSkew", "NContent", "ExonCount", "IntronCount",
                      "5pUTRlen", "3pUTRlen"]
            print >> out, "\t".join(header)
            for fields in premrna_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)

    # Process mature mRNAs
    if args.mrnas:
        a = args.mrnas
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa, \
                open(a[2], "w") as out:
            header = ["Species", "MrnaId", "Accession", "Length", "GCContent",
                      "GCSkew", "NContent"]
            print >> out, "\t".join(header)
            for fields in mrna_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)

    # Process coding sequences
    if args.cds:
        a = args.cds
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa, \
                open(a[2], "w") as out:
            header = ["Species", "CdsId", "MrnaId", "Length", "GCContent",
                      "GCSkew", "NContent"]
            print >> out, "\t".join(header)
            for fields in cds_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)

    # Process exons
    if args.exons:
        a = args.exons
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa, \
                open(a[2], "w") as out:
            header = ["Species", "ExonPos", "MrnaId", "Length", "GCContent",
                      "GCSkew", "NContent", "Context", "Phase", "Remainder"]
            print >> out, "\t".join(header)
            for fields in exon_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)

    # Process introns
    if args.introns:
        a = args.introns
        with open(a[0], "r") as gff, \
                open(a[1], "r") as fa, \
                open(a[2], "w") as out:
            header = ["Species", "IntronPos", "MrnaId", "Length", "GCContent",
                      "GCSkew", "NContent", "Context"]
            print >> out, "\t".join(header)
            for fields in intron_desc(gff, fa):
                fields = [args.species] + fields
                print >> out, "\t".join(fields)
