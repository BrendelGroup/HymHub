#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Nasonia vitripennis"
SPEC=Nvit
ORIGFASTA=${SPEC}.orig.fa.gz
ORIGGFF3=ref_Nvit_2.1_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-chromosome.sh
source src/ncbi-cleanup.sh

ASMBLFILES="CHR_Un/nvi_ref_Nvit_2.1_chrUn.fa.gz"
for i in {1..5}
do

  ASMBLFILES="$ASMBLFILES CHR_0${i}/nvi_ref_Nvit_2.1_chr${i}.fa.gz"
done
ncbi_download_chromosome
ncbi_cleanup

echo "[HymHub: $FULLSPEC] complete!"

