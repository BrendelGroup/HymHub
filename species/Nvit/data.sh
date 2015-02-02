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

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/ncbi-download-chromosome.sh
  ASMBLFILES="CHR_Un/nvi_ref_Nvit_2.1_chrUn.fa.gz"
  for i in {1..5}
  do

    ASMBLFILES="$ASMBLFILES CHR_0${i}/nvi_ref_Nvit_2.1_chr${i}.fa.gz"
  done
  ncbi_download_chromosome
fi

if [ "$DOFILTER" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format
fi

if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
