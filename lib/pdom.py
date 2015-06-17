#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""
Module for downloading unpublished Polistes dominula data.

Publication pending. Please be respectful and treat these data as you would
the unpublished data of a close colleague. HymHub will be updated soon when
these data are accessible from NCBI.
"""

import sys
import download as dld

ipbase = 'http://de.iplantcollaborative.org/dl/d'


def download(config, rootdir='.', logstream=sys.stderr):
    assert config['source'] == 'custom' and config['label'] == 'Pdom'
    download_scaffolds(config, rootdir=rootdir, logstream=logstream)
    download_annotations(config, rootdir=rootdir, logstream=logstream)
    download_proteins(config, rootdir=rootdir, logstream=logstream)


def download_scaffolds(config, rootdir='.', logstream=sys.stderr):
    logmsg = '[HymHub %s] download genome assembly' % config['species']
    if logstream is not None:
        print >> logstream, logmsg

    filename = config['genomeseq']['filename']
    url = '%s/%s/%s' % (ipbase, config['genomeseq']['prefix'], filename)
    outfile = '%s/species/Pdom/%s' % (rootdir, filename)
    dld.url_download(url, outfile)


def download_annotations(config, rootdir='.', logstream=sys.stderr):
    logmsg = '[HymHub %s] download genome annotation' % config['species']
    if logstream is not None:
        print >> logstream, logmsg

    filename = config['genomeannot']['filename']
    url = '%s/%s/%s' % (ipbase, config['genomeannot']['prefix'], filename)
    outfile = '%s/species/Pdom/%s' % (rootdir, filename)
    dld.url_download(url, outfile)


def download_proteins(config, rootdir='.', logstream=sys.stderr):
    logmsg = '[HymHub %s] download protein sequences' % config['species']
    if logstream is not None:
        print >> logstream, logmsg

    filename = config['protein']['filename']
    url = '%s/%s/%s' % (ipbase, config['protein']['prefix'], filename)
    outfile = '%s/species/Pdom/protein.fa.gz' % rootdir
    dld.url_download(url, outfile, compress=True)
