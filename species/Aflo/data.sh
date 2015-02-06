#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Apis florea"
SPEC=Aflo
ORIGFASTA=afl_ref_Aflo_1.0_chrUn.fa.gz
ORIGGFF3=ref_Aflo_1.0_top_level.gff3.gz

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/ncbi-download-scaffold.sh
  ncbi_download_scaffold
fi
if [ "$DOFORMAT" != "0" ]; then
  source src/ncbi-format.sh
  ncbi_format
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
