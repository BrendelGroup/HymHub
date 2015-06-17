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
import yaml

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
        download(url, outfile)


def download_annotation(config, rootdir='.', logstream=sys.stderr,
                        dryrun=False):
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
        download(url, outfile)


def download_proteins(config, rootdir='.', logstream=sys.stderr,
                      dryrun=False):
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
        download(url, outfile)


def download_flybase(config, rootdir='.', logstream=sys.stderr, dryrun=False):
    assert config['source'] == 'ncbi_flybase'
    species = config['species'].replace(' ', '_')

    logmsg = '[HymHub: %s] download genome data from NCBI' % config['species']
    if logstream is not None:  # pragma: no cover
        print >> logstream, logmsg

    chrs = list()
    anns = list()
    prts = list()
    chrout = '%s/species/%s/%s.orig.fa.gz' % (rootdir, config['label'],
                                              config['label'])
    annout = '%s/species/%s/%s' % (rootdir, config['label'],
                                   config['annotfile'])
    prtout = '%s/species/%s/protein.fa.gz' % (rootdir, config['label'])
    for acc in config['accessions']:
        base = '%s/%s/%s/%s' % (ncbibase, species, config['prefix'], acc)
        chrs.append(base + '.fna')
        anns.append(base + '.gff')
        prts.append(base + '.faa')
    if dryrun is True:  # pragma: no cover
        return (chrs, anns, prts, chrout, annout, prtout)
    else:
        with gzip.open(chrout, 'wb') as out:
            for url in chrs:
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, out)
                c.perform()
                c.close()
        with gzip.open(annout, 'wb') as out:
            for url in anns:
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, out)
                c.perform()
                c.close()
        with gzip.open(prtout, 'wb') as out:
            for url in prts:
                c = pycurl.Curl()
                c.setopt(c.URL, url)
                c.setopt(c.WRITEDATA, out)
                c.perform()
                c.close()


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------


def get_configs():
    """Unit test fixture."""

    configs = list()

    cfgstr = """
    species: 'Draconis occidentalis'
    label: 'Docc'
    source: 'ncbi'
    genomeseq:
        type: 'chromosomes'
        prefix: 'Assembled_chromosomes/seq'
        files:
            - 'docc_ref_1.6_1.fa.gz'
            - 'docc_ref_1.6_2.fa.gz'
            - 'docc_ref_1.6_3.fa.gz'
            - 'docc_ref_1.6_4.fa.gz'
            - 'docc_ref_1.6_5.fa.gz'
            - 'docc_ref_1.6_6.fa.gz'
            - 'docc_ref_1.6_7.fa.gz'
            - 'docc_ref_1.6_8.fa.gz'
    genomeannot:
        filename: 'ref_Draconis_occidentalis_1.6_top_level.gff3.gz'
    """
    configs.append(yaml.load(cfgstr))

    cfgstr = """
    species: 'Basiliscus vulgaris'
    label: 'Bvul'
    source: 'ncbi'
    genomeseq:
        type: 'scaffolds'
        filename: 'bv_ref_1.1_chrUn.fa.gz'
    genomeannot:
        filename: 'ref_Basiliscus_vulgaris_1.1_top_level.gff3.gz'
    """
    configs.append(yaml.load(cfgstr))

    cfgstr = """
    species: 'Equus monoceros'
    label: 'Emon'
    source: 'ncbi'
    genomeseq:
        type: 'scaffolds'
        filename: 'emon_ref_3.4_chrUn.fa.gz'
    genomeannot:
        filename: 'ref_Equus_monoceros_3.4_top_level.gff3.gz'
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
