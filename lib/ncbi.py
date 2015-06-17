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
import pycurl
import sys

ncbibase = 'ftp://ftp.ncbi.nih.gov/genomes'


def download(url, localpath):
    with open(localpath, 'wb') as out:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, out)
        c.perform()
        c.close()


def download_chromosomes(config, rootdir='.', logstream=sys.stderr,
                         dryrun=False):
    assert config['genomeseq']['source'] == 'ncbi_chromosomes'
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
        with open(outfile, 'wb') as out:
            for url in urls:
                c = pycurl.Curl()
                c.setopt(c.ENCODING, 'gzip')
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, out)
                c.perform()
                c.close()


def download_scaffolds(config, rootdir='.', logstream=sys.stderr,
                       dryrun=False):
    assert config['genomeseq']['source'] == 'ncbi_scaffolds'
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
        download(url, outfile)


def download_annotation(config, rootdir='.', logstream=sys.stderr,
                        dryrun=False):
    assert config['genomeannot']['source'] == 'ncbi'
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
        download(url, outfile)


def download_proteins(config, rootdir='.', logstream=sys.stderr,
                      dryrun=False):
    assert config['proteinseq']['source'] == 'ncbi'
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
        download(url, outfile)


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------


def get_configs():
    """Unit test fixture."""
    import yaml

    configs = list()

    cfgstr = """
    species: Draconis occidentalis
    label: Docc
    genomeseq:
        source: 'ncbi_chromosomes'
        prefix: 'Assembled_chromosomes/seq'
        files:
            - docc_ref_1.6_1.fa.gz
            - docc_ref_1.6_2.fa.gz
            - docc_ref_1.6_3.fa.gz
            - docc_ref_1.6_4.fa.gz
            - docc_ref_1.6_5.fa.gz
            - docc_ref_1.6_6.fa.gz
            - docc_ref_1.6_7.fa.gz
            - docc_ref_1.6_8.fa.gz
    genomeannot:
        filename: 'ref_Draconis_occidentalis_1.6_top_level.gff3.gz'
        source: 'ncbi'
    proteinseq:
        source: 'ncbi'
    """
    configs.append(yaml.load(cfgstr))

    cfgstr = """
    species: 'Basiliscus vulgaris'
    label: 'Bvul'
    genomeseq:
        filename: 'bv_ref_1.1_chrUn.fa.gz'
        source: 'ncbi_scaffolds'
    genomeannot:
        filename: 'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz'
        source: 'ncbi'
    proteinseq:
        source: 'ncbi'
    """
    configs.append(yaml.load(cfgstr))

    cfgstr = """
    species: 'Equus monoceros'
    label: 'Emon'
    genomeseq:
        filename: 'emon_ref_3.4_chrUn.fa.gz'
        source: 'ncbi_scaffolds'
    genomeannot:
        filename: 'ref_Equus_monoceros_3.4_top_level.gff3.gz'
        source: 'ncbi'
    proteinseq:
        source: 'ncbi'
    """
    configs.append(yaml.load(cfgstr))

    configs.append(yaml.load(open('species/Ador/data.yml', 'r')))

    return configs


def test_scaffolds():
    """NCBI scaffolds download"""
    configs = get_configs()

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/CHR_Un/'
            'ado_ref_Apis_dorsata_1.3_chrUn.fa.gz',
            './species/Ador/ado_ref_Apis_dorsata_1.3_chrUn.fa.gz')
    cmd = download_scaffolds(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_monoceros/CHR_Un/'
            'emon_ref_3.4_chrUn.fa.gz',
            './species/Emon/emon_ref_3.4_chrUn.fa.gz')
    cmd = download_scaffolds(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/CHR_Un/'
            'bv_ref_1.1_chrUn.fa.gz',
            '/some/path/species/Bvul/bv_ref_1.1_chrUn.fa.gz')
    cmd = download_scaffolds(config, rootdir='/some/path', logstream=None,
                             dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_chromosomes():
    """NCBI chromosome download"""
    configs = get_configs()

    config = configs[0]
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


def test_annot():
    """NCBI annotation download"""
    configs = get_configs()

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/GFF/'
            'ref_Apis_dorsata_1.3_top_level.gff3.gz',
            './species/Ador/ref_Apis_dorsata_1.3_top_level.gff3.gz')
    cmd = download_annotation(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_monoceros/GFF/'
            'ref_Equus_monoceros_3.4_top_level.gff3.gz',
            './species/Emon/ref_Equus_monoceros_3.4_top_level.gff3.gz')
    cmd = download_annotation(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/GFF/'
            'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz',
            '/another/path//species/Bvul/'
            'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz')
    cmd = download_annotation(config, rootdir='/another/path/', logstream=None,
                              dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)


def test_proteins():
    """NCBI protein download"""
    configs = get_configs()

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata/protein/'
            'protein.fa.gz',
            '/home/gandalf/HymHub/species/Ador/protein.fa.gz')
    cmd = download_proteins(config, rootdir='/home/gandalf/HymHub',
                            logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Equus_monoceros/protein/'
            'protein.fa.gz',
            './species/Emon/protein.fa.gz')
    cmd = download_proteins(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)

    config = configs.pop()
    test = ('ftp://ftp.ncbi.nih.gov/genomes/Basiliscus_vulgaris/protein/'
            'protein.fa.gz',
            './species/Bvul/protein.fa.gz')
    cmd = download_proteins(config, logstream=None, dryrun=True)
    assert cmd == test, 'filenames do not match\n%s\n%s\n' % (test, cmd)
