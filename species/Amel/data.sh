#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Apis mellifera"
SPEC=Amel
ORIGFASTA=${SPEC}.orig.fa.gz
ORIGGFF3=ref_Amel_4.5_top_level.gff3.gz

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/ncbi-download-chromosome.sh
  ASMBLFILES="CHR_Un/ame_ref_Amel_4.5_chrUn.fa.gz"
  for i in {1..16}
  do
    ASMBLFILES="$ASMBLFILES CHR_LG${i}/ame_ref_Amel_4.5_chrLG${i}.fa.gz"
  done
  ncbi_download_chromosome
fi

if [ "$DOFILTER" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format NC_001566.1
fi

if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
