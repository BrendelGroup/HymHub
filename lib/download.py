#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
"""Simple module for downloading remote data with PycURL."""

import gzip
import pycurl


def url_download(urldata, localpath, compress=False):
    """
    Helper function for downloading remote data files with PycURL.

    The first argument can be either a string (single URL) or a list (multiple
    URLs). The second argument is the path to which the downloaded data will
    be written, overwriting the existing file if present. The final argument
    indicates whether the incoming data stream should be encoded.
    """
    urls = urldata
    if not isinstance(urldata, list):
        urls = [urldata]

    openfunc = open
    if compress is True:
        openfunc = gzip.open

    with openfunc(localpath, 'wb') as out:
        for url in urls:
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, out)
            c.perform()
            c.close()
