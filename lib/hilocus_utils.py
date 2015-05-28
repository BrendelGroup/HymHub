#!/usr/bin/env python
import subprocess


def load_proteins(protids, specieslist, rootdir='.', suffix='rep-prot.fa'):
    """Load the specified protein sequences into memory."""

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
    def phylo_class(self):
        if len(self.species) == 1:
            return list(self.species)[0]

        if self.species == set(['Ador', 'Aflo', 'Amel',
                                'Bimp', 'Bter', 'Cflo',
                                'Hsal', 'Mrot', 'Nvit',
                                'Pdom', 'Sinv', 'Dmel',
                                'Tcas']):
            return 'Insects'

        hymdict = set(['Ador', 'Aflo', 'Amel',
                       'Bimp', 'Bter', 'Cflo',
                       'Hsal', 'Mrot', 'Nvit',
                       'Pdom', 'Sinv'])
        hymcount = 0
        for spec in list(hymdict):
            if spec in self.species:
                hymcount += 1
        if self.species == hymdict:
            return 'Hymenoptera'

        if self.species == set(['Ador', 'Aflo', 'Amel',
                                'Bimp', 'Bter', 'Mrot']):
            return 'Bees'

        if self.species == set(['Ador', 'Aflo', 'Amel',
                                'Bimp', 'Bter']):
            return 'Apidae'

        if self.species == set(['Ador', 'Aflo', 'Amel']):
            return 'Honeybees'

        if self.species == set(['Bimp', 'Bter']):
            return 'Bumblebees'

        if self.species == set(['Cflo', 'Hsal', 'Sinv']):
            return 'Ants'

        return 'Other'

    def __repr__(self):
        values = [str(len(self.iloci)), str(len(self.species)),
                  self.phylo_class, ','.join(self.iloci),
                  ','.join(self.species)]
        return '\t'.join(values)
