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
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/hymbase-download.sh
source src/hymbase-cleanup.sh

hymbase_download
hymbase_cleanup

echo "[HymHub: $FULLSPEC] complete!"

