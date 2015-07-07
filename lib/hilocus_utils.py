#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

import os
import re
import subprocess
import fasta_utils


def prep_phylo(outdir, quartetfile, rootdir='.'):
    os.makedirs(outdir)
    next(quartetfile)
    for line in quartetfile:
        hilocusid, ant, bee, pdom, nvit = line.rstrip().split('\t')
        species = list()
        iloci = list()
        for value in [ant, bee, pdom, nvit]:
            spec, ilocus = value.split(':')
            species.append(spec)
            iloci.append(ilocus)
        protids = resolve_protein_ids(iloci, species, rootdir=rootdir)
        protseqs = list()
        for defline, protseq in retrieve_proteins(protids, species,
                                                  rootdir=rootdir):
            if not protseq.startswith('M'):
                continue
            defline = re.sub(r'>(gnl\|(Acep|Aech|Cflo|Hsal|Pbar|Sinv)\|[^\n])+',
                             r'>ant \1', defline)
            defline = re.sub(r'>(gnl\|(Ador|Aflo|Amel|Bimp|Bter|Mrot)\|[^\n])+',
                             r'>bee \1', defline)
            defline = re.sub(r'>(gnl\|Pdom\|[^\n])+', r'>vespid \1', defline)
            defline = re.sub(r'>(gnl\|Nvit\|[^\n])+', r'>chalcid \1', defline)
            protseqs.extend((defline, protseq))
        if len(protseqs) != 8:  # 4 sequences * 2 values (defline + sequence)
            continue

        os.makedirs(outdir + '/' + hilocusid)
        seqfile = '%s/%s/%s.faa' % (outdir, hilocusid, hilocusid)
        with open(seqfile, 'w') as outstream:
            print >> outstream, '\n'.join(protseqs)


def run_msa(proteinseqs, outfile=None, command='clustalo', path=None,
            outfmt='clustal', refmt=False):
    """
    Align the specified protein sequences using clustalo.
    """

    if refmt:
        proteinseqs = re.sub(r'>(gnl\|(....)\|\S+)', r'>\2 \1', proteinseqs)
    program = command
    if path is not None:
        program = path + '/' + command
    args = [program, '--seqtype=Protein', '--infile=-', '--outfmt=' + outfmt]
    if outfile is not None:
        args.append('--outfile=' + outfile)
    proc = subprocess.Popen(args, stdin=subprocess.PIPE)
    proc.communicate(input=proteinseqs)


def retrieve_proteins(protids, specieslist, rootdir='.', suffix='rep-prot.fa'):
    """Retrieve the specified protein sequences."""

    proteinseqs = ''
    for species in specieslist:
        filename = '%s/species/%s/%s.%s' % (rootdir, species, species, suffix)
        for defline, seq in fasta_utils.parse_fasta(open(filename, 'r')):
            pid = defline.split(' ')[0].split('|')[2]
            if pid in protids:
                yield defline, seq


def load_proteins(protids, specieslist, rootdir='.', suffix='rep-prot.fa'):
    """Load the specified protein sequences into memory."""

    proteinseqs = ''
    for species in specieslist:
        filename = '%s/species/%s/%s.%s' % (rootdir, species, species, suffix)
        for defline, seq in fasta_utils.parse_fasta(open(filename, 'r')):
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
    """Extract a hiLocus from the data table."""

    filename = rootdir + '/' + filepath
    for line in open(filename, 'r'):
        values = line.rstrip().split()
        if values[0] == hid:
            return values


def species_from_defline(defline):
    """
    Protein Fasta records in HymHub all follow the defline format
    >gnl|$species|$accession. This function defines the species property as
    parsed from the defline.
    """
    values = defline.split('|')
    assert len(values) == 3, \
        'Unable to parse species from defline: "%s"' % defline
    return values[1]


class hiLocus():
    """
    This class represents an entry in the HymHub hiLoci table.
    """

    def __init__(self, seqlist, prot_loc_map):
        self.iloci = [prot_loc_map[x.accession] for x in seqlist]
        self.species = set([species_from_defline(x.defline) for x in seqlist])

    @property
    def phylo_dist(self):
        dist = {'Acep': 0, 'Ador': 0, 'Aech': 0,
                'Aflo': 0, 'Amel': 0, 'Bimp': 0,
                'Bter': 0, 'Cflo': 0, 'Hsal': 0,
                'Mrot': 0, 'Nvit': 0, 'Pbar': 0,
                'Pdom': 0, 'Sinv': 0, 'Dmel': 0,
                'Tcas': 0}
        for s in self.species:
            assert s in dist
            dist[s] = 1
        profile = ''
        for species in sorted(dist):
            if profile != '':
                profile += '\t'
            profile += str(dist[species])
        return profile

    @property
    def in_apis(self):
        count = 0
        for spec in ['Ador', 'Aflo', 'Amel']:
            if spec in self.species:
                count += 1
        return count

    @property
    def in_bombus(self):
        count = 0
        for spec in ['Bimp', 'Bter']:
            if spec in self.species:
                count += 1
        return count

    @property
    def in_apidae(self):
        return self.in_apis + self.in_bombus

    @property
    def in_bees(self):
        count = self.in_apidae
        if 'Mrot' in self.species:
            count += 1
        return count

    @property
    def in_ants(self):
        count = 0
        for spec in ['Acep', 'Aech', 'Cflo', 'Hsal', 'Pbar', 'Sinv']:
            if spec in self.species:
                count += 1
        return count

    @property
    def in_outgroups(self):
        count = 0
        for spec in ['Dmel', 'Tcas']:
            if spec in self.species:
                count += 1
        return count

    @property
    def in_hymenoptera(self):
        count = self.in_ants + self.in_bees
        for spec in ['Pdom', 'Nvit']:
            if spec in self.species:
                count += 1
        return count

    @property
    def phylo_class(self):
        if len(self.species) == 1:
            return 'Orphan'
        if self.in_hymenoptera > 0 and self.in_outgroups > 0:
            return 'Insects'
        if self.in_hymenoptera == 0 and self.in_outgroups == 2:
            return 'NonHymenoptera'
        assert self.in_outgroups == 0

        if self.in_apidae > 0 and 'Mrot' in self.species and \
           self.in_hymenoptera == self.in_bees:
            return 'Bees'
        if self.in_apis > 1 and self.in_bombus > 0 and \
           self.in_hymenoptera == self.in_apidae:
            return 'Apidae'
        if self.in_apis > 1 and self.in_hymenoptera == self.in_apis:
            return 'Honeybees'
        if self.in_bombus > 1 and self.in_hymenoptera == self.in_bombus:
            return 'Bumblebees'
        if self.in_bees > 1 and self.in_hymenoptera == self.in_bees:
            return 'SomeBees'

        if self.in_ants > 1 and self.in_hymenoptera == self.in_ants:
            return 'Ants'

        if self.in_bees > 0 and self.in_ants > 0 and \
           self.in_hymenoptera == self.in_bees + self.in_ants:
            return 'AntsAndBees'

        if self.in_bees > 0 and 'Pdom' in self.species and \
           self.in_hymenoptera == self.in_bees + 1:
            return 'BeesAndWasps'

        if self.in_ants > 0 and 'Pdom' in self.species and \
           self.in_hymenoptera == self.in_ants + 1:
            return 'AntsAndWasps'

        if self.in_ants > 0 and self.in_bees > 0 and \
           ('Pdom' in self.species or 'Nvit' in self.species):
            return 'Hymenoptera'

        return 'Other'

    def __repr__(self):
        values = [str(len(self.iloci)), str(len(self.species)),
                  self.phylo_class, ','.join(self.iloci),
                  ','.join(self.species)]
        return '\t'.join(values)
