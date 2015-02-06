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
  root="Assembled_chromosomes/seq"
  ASMBLFILES=""
  for i in chr1 chr2 chr3 chr4 chr5 unlocalized unplaced
  do
    ASMBLFILES="$ASMBLFILES ${root}/nvi_ref_Nvit_2.1_${i}.fa.gz"
  done
  ncbi_download_chromosome
fi

if [ "$DOFORMAT" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format GeneID:100498670
fi

if [ "$DODATATYPES" != "0" ]; then
  source src/datatypes.sh
  get_datatypes $SPEC
fi

if [ "$DOSTATS" != "0" ]; then
  source src/stats.sh
  get_stats $SPEC
fi

if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
