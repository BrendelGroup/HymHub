#!/usr/bin/env python

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

from __future__ import print_function
import argparse
import re
import sys

for line in sys.stdin:
    liilmatch = re.search('liil=(\d+)', line)
    riilmatch = re.search('riil=(\d+)', line)
    if not liilmatch or not riilmatch:
        continue

    liil = int(liilmatch.group(1))
    riil = int(riilmatch.group(1))
    print("%d\t%d" % (liil, riil))
