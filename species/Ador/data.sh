#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Apis dorsata"
SPEC=Aflo
FULLSPEC="Apis dorsata"
SPEC=Ador
NCBIBASE=ftp://ftp.ncbi.nih.gov/genomes/Apis_dorsata
ORIGFASTA=ado_ref_Apis_dorsata_1.3_chrUn.fa.gz
ORIGGFF3=ref_Apis_dorsata_1.3_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-scaffold.sh
source src/ncbi-cleanup.sh

ncbi_download_scaffold
ncbi_cleanup

echo "[HymHub: $FULLSPEC] complete!"

