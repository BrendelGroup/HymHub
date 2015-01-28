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
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/hymbase-download.sh
source src/hymbase-cleanup.sh

hymbase_download
hymbase_cleanup

echo "[HymHub: $FULLSPEC] complete!"

