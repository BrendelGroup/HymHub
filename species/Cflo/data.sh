#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Camponotus floridanus"
SPEC=Cflo
URLGENUS="camponotus"
ORIGFASTA=Cflo_3.3_scaffolds.fa.gz
ORIGGFF3=cflo_OGSv3.3.gff3.gz

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
  hymbase_format 'C3809596|C3873680'
fi
if [ "$DODATATYPES" != "0" ]; then
  source src/datatypes.sh
  get_datatypes $SPEC
fi
if [ "$DOCLEANUP" != "0" ]; then
  source src/cleanup.sh
  data_cleanup
fi

echo "[HymHub: $FULLSPEC] complete!"
