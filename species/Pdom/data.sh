#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Polistes dominula"
SPEC=Pdom
PdomDataStore=/iplant/home/standage/Polistes_dominula/r1.2
WD=$1

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh

if [ "$DODOWNLOAD" != "0" ]; then
  echo "[HymHub: $FULLSPEC] download genome assembly"
  seqfile=pdom-scaffolds-unmasked-r1.2.fa.gz
  iget ${PdomDataStore}/genome-assembly/${seqfile} ${WD}/${seqfile}

  echo "[HymHub: $FULLSPEC] downloading genome annotation"
  iget ${PdomDataStore}/genome-annotation/pdom-annot-r1.2.gff3 ${WD}/.
fi

if [ "$DOFORMAT" != "0" ]; then
  echo "[HymHub: $FULLSPEC] renaming data files"
  cp ${WD}/pdom-scaffolds-unmasked-r1.2.fa.gz ${WD}/Pdom.gdna.fa.gz
  gunzip -f ${WD}/Pdom.gdna.fa.gz

  cp ${WD}/pdom-annot-r1.2.gff3 ${WD}/Pdom.gff3

  echo "[HymHub: $FULLSPEC] verify data files"
  shasum -c species/${SPEC}/checksums.sha
fi

if [ "$DODATATYPES" != "0" ]; then
  source src/datatypes.sh
  get_datatypes $SPEC
fi

if [ "$DOCLEANUP" != "0" ]; then
  echo "[HymHub: $FULLSPEC] clean up temporary files"
  find $WD -type f \
      | grep -v "/checksums.sha$" | grep -v "/data.sh$" \
      | grep -v "/${SPEC}.gdna.fa$" | grep -v "/${SPEC}.gff3$" \
      | xargs -n 1 rm -f || true
fi

echo "[HymHub: $FULLSPEC] complete!"
