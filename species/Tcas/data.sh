#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Tribolium castaneum"
SPEC=Tcas
ORIGFASTA=Tcas.orig.fa.gz
ORIGGFF3=ref_Tcas_3.0_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-chromosome.sh
source src/ncbi-cleanup.sh

ASMBLFILES=""
for i in Un 'LG1=X'
do
  ASMBLFILES="$ASMBLFILES CHR_${i}/tca_ref_Tcas_3.0_chr${i}.fa.gz"
done
for i in {2..10}
do
  ASMBLFILES="$ASMBLFILES CHR_LG${i}/tca_ref_Tcas_3.0_chrLG${i}.fa.gz"
done
ncbi_download_chromosome
ncbi_cleanup NC_003081.2

echo "[HymHub: $FULLSPEC] complete!"

