#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""
Module for downloading genome data from NCBI.

Simple module for downloading genome assemblies, annotations, and proteins from
NCBI's FTP site. The unit tests validate the behavior of this module with a mix
of real and bogus data configurations.
"""

import gzip
import subprocess
import sys
import yaml
import download

ncbibase = 'ftp://ftp.ncbi.nih.gov/genomes'


def download_chromosomes(config, rootdir='.', logstream=sys.stderr,
                         dryrun=False):
    """Download chromosome-based genome sequences from NCBI."""
    assert config['source'] == 'ncbi' and \
        config['genomeseq']['type'] == 'chromosomes'
    species = config['species'].replace(' ', '_')

    logmsg = '[HymHub: %s] download genome from NCBI' % config['species']
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    urls = list()
    prefix = config['genomeseq']['prefix']
    for remotefile in config['genomeseq']['files']:
        url = '%s/%s/%s/%s' % (ncbibase, species, prefix, remotefile)
        urls.append(url)
    outfile = '%s/species/%s/%s.orig.fa.gz' % (rootdir, config['label'],
                                               config['label'])
    if dryrun is True:  # pragma: no cover
        return urls, outfile
    else:
        download.url_download(urls, outfile)


def download_scaffolds(config, rootdir='.', logstream=sys.stderr,
                       dryrun=False):
    """Download scaffold-based genome sequences from NCBI."""
    assert config['source'] == 'ncbi' and \
        config['genomeseq']['type'] == 'scaffolds'
    species = config['species'].replace(' ', '_')

    logmsg = '[HymHub: %s] download genome from NCBI' % config['species']
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    filename = config['genomeseq']['filename']
    url = '%s/%s/CHR_Un/%s' % (ncbibase, species, filename)
    outfile = '%s/species/%s/%s' % (rootdir, config['label'], filename)
    if dryrun is True:  # pragma: no cover
        return url, outfile
    else:
        download.url_download(url, outfile)


def download_annotation(config, rootdir='.', logstream=sys.stderr,
                        dryrun=False):
    """Download genome annotation from NCBI."""
    assert config['source'] == 'ncbi'
    species = config['species'].replace(' ', '_')

    logmsg = '[HymHub: %s] download annotation from NCBI' % config['species']
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    filename = config['genomeannot']['filename']
    url = '%s/%s/GFF/%s' % (ncbibase, species, filename)
    outfile = '%s/species/%s/%s' % (rootdir, config['label'], filename)
    if dryrun is True:  # pragma: no cover
        return url, outfile
    else:
        download.url_download(url, outfile)


def download_proteins(config, rootdir='.', logstream=sys.stderr,
                      dryrun=False):
    """Download protein sequences from NCBI."""
    assert config['source'] == 'ncbi'
    species = config['species'].replace(' ', '_')

    logmsg = ('[HymHub: %s] download protein sequences from NCBI' %
              config['species'])
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    url = '%s/%s/protein/protein.fa.gz' % (ncbibase, species)
    outfile = '%s/species/%s/protein.fa.gz' % (rootdir, config['label'])
    if dryrun is True:  # pragma: no cover
        return url, outfile
    else:
        download.url_download(url, outfile)


def download_flybase(config, rootdir='.', logstream=sys.stderr, dryrun=False):
    """
    Download Drosophila data from NCBI.

    Genome sequences and annotations for Drosophila melanogaster in NCBI are
    organized differently than for most other species, presumably since they
    are sourced from FlyBase. This function downloads all of the genome
    sequences, annotations, and protein sequences for Dmel.
    """
    assert config['source'] == 'ncbi_flybase'
    species = config['species'].replace(' ', '_')

    logmsg = '[HymHub: %s] download genome data from NCBI' % config['species']
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    chrs, anns, tmps, prts = list(), list(), list(), list()
    chrout = '%s/species/%s/%s.orig.fa.gz' % (rootdir, config['label'],
                                              config['label'])
    prtout = '%s/species/%s/protein.fa.gz' % (rootdir, config['label'])
    annout = '%s/species/%s/%s' % (rootdir, config['label'],
                                   config['annotfile'])
    for acc in config['accessions']:
        base = '%s/%s/%s/%s' % (ncbibase, species, config['prefix'], acc)
        chrs.append(base + '.fna')
        prts.append(base + '.faa')
        anns.append(base + '.gff')
        tmps.append('%s/species/%s/%s.gff.gz' % (rootdir, config['label'],
                    acc.split('/')[1]))
    if dryrun is True:  # pragma: no cover
        return (chrs, anns, prts, chrout, annout, prtout)
    else:
        download.url_download(chrs, chrout, compress=True)
        download.url_download(prts, prtout, compress=True)
        for annremote, annlocal in zip(anns, tmps):
            download.url_download(annremote, annlocal, compress=True)

        with gzip.open(annout, 'wb') as outfile:
            cmd = 'gt gff3 -sort -tidy ' + ' '.join(tmps)
            proc = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
            for line in proc.stdout:
                outfile.write(line)


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------


def test_scaffolds():
    """NCBI scaffolds download"""
    config = config = yaml.load(open('test/Emon.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_monoceros/CHR_Un/'
            'emon_ref_3.4_chrUn.fa.gz',
            './species/Emon/emon_ref_3.4_chrUn.fa.gz')
    cmd = download_scaffolds(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('test/Bvul.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/CHR_Un/'
            'bv_ref_1.1_chrUn.fa.gz',
            '/some/path/species/Bvul/bv_ref_1.1_chrUn.fa.gz')
    cmd = download_scaffolds(config, rootdir='/some/path', logstream=None,
                             dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('species/Ador/data.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/CHR_Un/'
            'ado_ref_Apis_dorsata_1.3_chrUn.fa.gz',
            './species/Ador/ado_ref_Apis_dorsata_1.3_chrUn.fa.gz')
    cmd = download_scaffolds(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_chromosomes():
    """NCBI chromosome download"""
    config = config = yaml.load(open('test/Docc.yml', 'r'))
    urls = ['docc_ref_1.6_1.fa.gz', 'docc_ref_1.6_2.fa.gz',
            'docc_ref_1.6_3.fa.gz', 'docc_ref_1.6_4.fa.gz',
            'docc_ref_1.6_5.fa.gz', 'docc_ref_1.6_6.fa.gz',
            'docc_ref_1.6_7.fa.gz', 'docc_ref_1.6_8.fa.gz']
    prefix = ('ftp://ftp.ncbi.nih.gov/genomes/Draconis_occidentalis/'
              'Assembled_chromosomes/seq/')
    urls = [prefix + x for x in urls]
    test = (urls, './species/Docc/Docc.orig.fa.gz')
    cmd = download_chromosomes(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('test/Epeg.yml', 'r'))
    urls = ['epeg_reg_Epe_2.1_01.fa.gz', 'epeg_reg_Epe_2.1_02.fa.gz',
            'epeg_reg_Epe_2.1_03.fa.gz', 'epeg_reg_Epe_2.1_04.fa.gz',
            'epeg_reg_Epe_2.1_05.fa.gz', 'epeg_reg_Epe_2.1_06.fa.gz',
            'epeg_reg_Epe_2.1_07.fa.gz', 'epeg_reg_Epe_2.1_08.fa.gz',
            'epeg_reg_Epe_2.1_09.fa.gz', 'epeg_reg_Epe_2.1_10.fa.gz',
            'epeg_reg_Epe_2.1_11.fa.gz', 'epeg_reg_Epe_2.1_12.fa.gz']
    prefix = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_pegasus/'
              'Assembled_chromosomes/seq/')
    urls = [prefix + x for x in urls]
    test = (urls, './species/Epeg/Epeg.orig.fa.gz')
    cmd = download_chromosomes(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_annot():
    """NCBI annotation download"""
    config = config = yaml.load(open('test/Bvul.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/GFF/'
            'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz',
            '/another/path//species/Bvul/'
            'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz')
    cmd = download_annotation(config, rootdir='/another/path/', logstream=None,
                              dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('test/Epeg.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_pegasus/GFF/'
            'ref_EPEG_2.1_top_level.gff3.gz',
            './species/Epeg/ref_EPEG_2.1_top_level.gff3.gz')
    cmd = download_annotation(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('species/Ador/data.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/GFF/'
            'ref_Apis_dorsata_1.3_top_level.gff3.gz',
            './species/Ador/ref_Apis_dorsata_1.3_top_level.gff3.gz')
    cmd = download_annotation(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_proteins():
    """NCBI protein download"""
    config = config = yaml.load(open('test/Emon.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_monoceros/protein/'
            'protein.fa.gz',
            './species/Emon/protein.fa.gz')
    cmd = download_proteins(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = config = yaml.load(open('test/Bvul.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/protein/'
            'protein.fa.gz',
            './species/Bvul/protein.fa.gz')
    cmd = download_proteins(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = yaml.load(open('species/Ador/data.yml', 'r'))
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/protein/'
            'protein.fa.gz',
            '/home/gandalf/HymHub/species/Ador/protein.fa.gz')
    cmd = download_proteins(config, rootdir='/home/gandalf/HymHub',
                            logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_flybase():
    """NCBI FlyBase data download"""
    config = yaml.load(open('species/Dmel/data.yml', 'r'))
    bases = ['CHR_X/NC_004354', 'CHR_2/NT_033778', 'CHR_2/NT_033779',
             'CHR_3/NT_033777', 'CHR_3/NT_037436', 'CHR_4/NC_004353']
    prefix = ('ftp://ftp.ncbi.nih.gov/genomes/Drosophila_melanogaster/'
              'RELEASE_5_48/')
    chrs = [prefix + x + '.fna' for x in bases]
    anns = [prefix + x + '.gff' for x in bases]
    prts = [prefix + x + '.faa' for x in bases]
    test = (chrs, anns, prts, './species/Dmel/Dmel.orig.fa.gz',
            './species/Dmel/dmel-5.48-ncbi.gff3.gz',
            './species/Dmel/protein.fa.gz')
    cmd = download_flybase(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)
