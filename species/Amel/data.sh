#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Apis mellifera"
SPEC=Amel
ORIGFASTA=Amel.orig.fa.gz
ORIGGFF3=ref_Amel_4.5_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-chromosome.sh
source src/ncbi-cleanup.sh

ASMBLFILES="CHR_Un/ame_ref_Amel_4.5_chrUn.fa.gz"
for i in {1..16}
do
  ASMBLFILES="$ASMBLFILES CHR_LG${i}/ame_ref_Amel_4.5_chrLG${i}.fa.gz"
done
ncbi_download_chromosome
ncbi_cleanup NC_001566.1

echo "[HymHub: $FULLSPEC] complete!"

