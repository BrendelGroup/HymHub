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

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/ncbi-download-chromosome.sh
  root="Assembled_chromosomes/seq"
  ASMBLFILES="${root}/bte_ref_Bter_1.0_unplaced.fa.gz"
  for i in {1..9}
  do
    ASMBLFILES="$ASMBLFILES ${root}/bte_ref_Bter_1.0_chrLG_B0${i}.fa.gz"
  done
  for i in {10..18}
  do
    ASMBLFILES="$ASMBLFILES ${root}/bte_ref_Bter_1.0_chrLG_B${i}.fa.gz"
  done
  ncbi_download_chromosome
fi

if [ "$DOFORMAT" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format
fi

if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
