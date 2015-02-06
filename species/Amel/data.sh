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
  root="Assembled_chromosomes/seq"
  ASMBLFILES="${root}/ame_ref_Amel_4.5_unplaced.fa.gz"
  for i in {1..16}
  do
    ASMBLFILES="$ASMBLFILES ${root}/ame_ref_Amel_4.5_chrLG${i}.fa.gz"
  done
  ncbi_download_chromosome
fi

if [ "$DOFORMAT" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format NC_001566.1
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
