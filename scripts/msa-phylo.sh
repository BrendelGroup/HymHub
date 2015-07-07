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
prefix=$(basename $1)

# Multiple sequence alignment with Clustal Omega
cat ${prefix}.faa | clustalo --seqtype=Protein --infile=- --outfmt=phylip > infile

# Phylogeny inference with PHYLIP
#   uses default input file `infile`
#
#   O 4: root tree with sequence 4 (Nasonia) as outgroup
#   S:   disable speedy/rough mode
#   Y:   accept parameters and launch
echo $'O\n4\nS\nY' | proml

# Drawing phylogenetic tree
echo "outtree" >> tmp-drawtree.par
echo "/usr/local/src/PHY-DIR/PHYLIP/phylip-3.69/src/font1" >> tmp-drawtree.par
echo "V" >> tmp-drawtree.par
echo "N" >> tmp-drawtree.par
echo "L" >> tmp-drawtree.par
echo "R" >> tmp-drawtree.par
echo "D" >> tmp-drawtree.par
echo "Y" >> tmp-drawtree.par
cat tmp-drawtree.par | drawtree
mv plotfile ${hid}.ps
rm tmp-drawtree.par
ps2pdf ${hid}.ps
