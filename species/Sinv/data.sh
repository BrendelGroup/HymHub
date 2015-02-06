#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Solenopsis invicta"
SPEC=Sinv
URLGENUS="solenopsis"
ORIGFASTA=Sinv_1.0_scaffolds.fa.gz
ORIGGFF3=sinv_OGSv2.2.3.gff3.gz

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  source src/hymbase-download.sh
  hymbase_download
fi
if [ "$DOFORMAT" != "0" ]; then
  source src/hymbase-format.sh
  hymbase_format NC_014672.1
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
