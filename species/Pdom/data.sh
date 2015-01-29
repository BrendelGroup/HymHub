#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Polistes dominula"
PdomDataStore=/iplant/home/standage/Polistes_dominula/r1.2
WD=$1

# Procedure
#-------------------------------------------------------------------------------

echo "[HymHub: $FULLSPEC] download genome assembly"
iget ${PdomDataStore}/genome-assembly/pdom-scaffolds-unmasked-r1.2.fa.gz ${WD}/.

echo "[HymHub: $FULLSPEC] downloading genome annotation"
iget ${PdomDataStore}/genome-annotation/pdom-annot-r1.2.gff3 ${WD}/.

echo "[HymHub: $FULLSPEC] renaming data files"
mv ${WD}/pdom-scaffolds-unmasked-r1.2.fa.gz ${WD}/Pdom.gdna.fa.gz
gunzip ${WD}/Pdom.gdna.fa.gz
mv ${WD}/pdom-annot-r1.2.gff3 ${WD}/Pdom.gff3

echo "[HymHub: $FULLSPEC] complete!"

