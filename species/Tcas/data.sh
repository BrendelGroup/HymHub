#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Tribolium castaneum"
SPEC=Tcas
ORIGFASTA=${SPEC}.orig.fa.gz
ORIGGFF3=ref_Tcas_3.0_top_level.gff3.gz

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/ncbi-download-chromosome.sh
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
fi

if [ "$DOFORMAT" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format NC_003081.2
fi

if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
