#!/usr/bin/env python
"""

"""

import cdhit


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

        if self.species == set([ 'Ador', 'Aflo', 'Amel',
                                 'Bimp', 'Bter', 'Cflo',
                                 'Hsal', 'Mrot', 'Nvit',
                                 'Pdom', 'Sinv', 'Dmel',
                                 'Tcas' ]):
            return 'Insects'

        hymdict = set([ 'Ador', 'Aflo', 'Amel',
                        'Bimp', 'Bter', 'Cflo',
                        'Hsal', 'Mrot', 'Nvit',
                        'Pdom', 'Sinv' ])
        hymcount = 0
        for spec in list(hymdict):
            if spec in self.species:
                hymcount += 1
        if self.species == hymdict:
            return 'Hymenoptera'

        if self.species == set([ 'Ador', 'Aflo', 'Amel',
                                 'Bimp', 'Bter', 'Mrot' ]):
            return 'Bees'

        if self.species == set([ 'Ador', 'Aflo', 'Amel',
                                 'Bimp', 'Bter' ]):
            return 'Apidae'

        if self.species == set([ 'Ador', 'Aflo', 'Amel' ]):
            return 'Honeybees'

        if self.species == set([ 'Bimp', 'Bter' ]):
            return 'Bumblebees'

        if self.species == set([ 'Cflo', 'Hsal', 'Sinv' ]):
            return 'Ants'

        return 'Other'

    def __repr__(self):
        values = [str(len(self.iloci)), str(len(self.species)),
                  self.phylo_class, ','.join(self.iloci),
                  ','.join(self.species)]
        return '\t'.join(values)


if __name__ == "__main__":
    """
    Script for creating HymHub's hiLocus data table.
    """
    import argparse
    import sys

    desc = 'Parse CD-HIT output to determine hiLoci'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
            default=sys.stdout, dest='outfile',
            help='output file name; default is terminal (stdout)')
    parser.add_argument('-m', '--mint', type=str, default=None,
            metavar='format',
            help='Mint unique IDs for each hiLocus with the given '
                 'printf-style format')
    parser.add_argument('cdhitfile', type=argparse.FileType('r'),
            help='protein clustering (output file from CD-HIT)')
    parser.add_argument('mapping', type=argparse.FileType('r'),
            help='mapping of protein IDs/accessions to iLocus IDs')
    args = parser.parse_args()

    prot2loci = dict()
    for line in args.mapping:
        protid, locid = line.rstrip().split('\t')
        prot2loci[protid] = locid

    
    header = ['iLocusCount', 'SpeciesCount',
              'PhylogeneticClassification', 'iLoci', 'Species']
    if args.mint is not None:
        header = ['ID', 'Label'] + header
        count = 0
    print >> args.outfile, '\t'.join(header)
    for clusterid, clusterseqs in cdhit.parse_clusters(args.cdhitfile):
        hl = hiLocus(clusterseqs, prot2loci)
        if args.mint is not None:
            count += 1
            uid = args.mint % count
            args.outfile.write('%s\t%s\t' % (uid, uid))
        args.outfile.write('%s\n' % hl)
