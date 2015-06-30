#!/usr/bin/env bash

# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
#
# Run multiple sequence alignment and phylogeny inference.
# Usage: bash msa-phylo.sh hiLocusID/
set -eo pipefail

which clustalo
which proml

cd $1
cat $1.faa | clustalo --seqtype=Protein --infile=- --outfmt=phylip > infile
echo $'O\n4\nS\nY' | proml
