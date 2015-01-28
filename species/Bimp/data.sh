#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Bombus impatiens"
SPEC=Bimp
ORIGFASTA=bim_ref_BIMP_2.0_chrUn.fa.gz
ORIGGFF3=ref_BIMP_2.0_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-scaffold.sh
source src/ncbi-cleanup.sh

ncbi_download_scaffold
ncbi_cleanup

echo "[HymHub: $FULLSPEC] complete!"

