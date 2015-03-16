#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Apis mellifera OGS 3.2"
SPEC=Am32
URLGENUS="beebase"
ORIGFASTA=Amel_4.5_scaffolds.fa.gz
ORIGGFF3=amel_OGSv3.2.gff3.gz

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  HYMBASE=http://hymenopteragenome.org/beebase/sites/hymenopteragenome.org.beebase/files/data
    
  echo "[HymHub: $FULLSPEC] download genome from HymenopteraBase"
  curl ${HYMBASE}/${ORIGFASTA} > $refrfasta 2> ${refrfasta}.log
  
  echo "[HymHub: $FULLSPEC] download annotation from HymenopteraBase"
  curl ${HYMBASE}/consortium_data/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
fi
if [ "$DOFORMAT" != "0" ]; then
  source src/hymbase-format.sh
  hymbase_format GB44324
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
