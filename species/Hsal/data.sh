#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Harpegnathos saltator"
SPEC=Hsal
NCBIBASE=ftp://ftp.ncbi.nih.gov/genomes/Harpegnathos_saltator
ORIGFASTA=hsa_ref_HarSal_1.0_chrUn.fa.gz
ORIGGFF3=ref_HarSal_1.0_top_level.gff3.gz
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/filenames.sh
source src/ncbi-download-scaffold.sh
source src/ncbi-cleanup.sh

ncbi_download_scaffold
ncbi_cleanup

echo "[HymHub: $FULLSPEC] complete!"

