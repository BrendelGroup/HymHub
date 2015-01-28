#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Bombus terrestris"
SPEC=Bter
ORIGFASTA=${SPEC}.orig.fa.gz
ORIGGFF3=ref_Bter_1.0_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-chromosome.sh
source src/ncbi-cleanup.sh

ASMBLFILES="CHR_Un/bte_ref_Bter_1.0_chrUn.fa.gz"
for i in {1..9}
do
  ASMBLFILES="$ASMBLFILES CHR_LG_B0${i}/bte_ref_Bter_1.0_chrLG_B0${i}.fa.gz"
done
for i in {10..18}
do
  ASMBLFILES="$ASMBLFILES CHR_LG_B${i}/bte_ref_Bter_1.0_chrLG_B${i}.fa.gz"
done
ncbi_download_chromosome
ncbi_cleanup

echo "[HymHub: $FULLSPEC] complete!"

