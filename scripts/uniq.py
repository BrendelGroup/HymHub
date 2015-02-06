#!/usr/bin/env python
# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
import sys
lines = {}
for line in sys.stdin:
  if line in lines:
    continue
  lines[line] = 1
  print line
