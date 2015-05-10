#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Polistes dominula"
SPEC=Pdom
MODE="hymbase"

# Procedure
#-------------------------------------------------------------------------------
source src/data-cli.sh
source src/filenames.sh

if [ "$DODOWNLOAD" != "0" ]; then
  echo "[HymHub: $FULLSPEC] download genome assembly"
  seqfile=pdom-scaffolds-unmasked-r1.2.fa.gz
  curl ${IPLNT}/53B7319E-3201-4087-9607-2D541FF34DD0/${seqfile} \
      > ${WD}/${seqfile} 2> ${WD}/${seqfile}.log

  echo "[HymHub: $FULLSPEC] download protein sequences"
  protfile=pdom-annot-r1.2-proteins.fa
  curl ${IPLNT}/ACD29139-6619-48DF-A9F2-F75CA382E248/${protfile} \
      2> ${WD}/protein.log \
      | gzip -c > ${WD}/protein.fa.gz

  echo "[HymHub: $FULLSPEC] downloading genome annotation"
  featfile=pdom-annot-r1.2.gff3
  curl ${IPLNT}/E4944CBB-7DE4-4CA1-A889-3D2A5D2E8696/${featfile} \
      > ${WD}/${featfile} 2> ${WD}/${featfile}.log
fi

if [ "$DOFORMAT" != "0" ]; then
  echo "[HymHub: $FULLSPEC] renaming data files"
  cp ${WD}/pdom-scaffolds-unmasked-r1.2.fa.gz ${WD}/Pdom.gdna.fa.gz
  gunzip -f ${WD}/Pdom.gdna.fa.gz
  gunzip -c ${WD}/protein.fa.gz > ${WD}/Pdom.prot.fa

  cp ${WD}/pdom-annot-r1.2.gff3 ${WD}/Pdom.gff3

  echo "[HymHub: $FULLSPEC] verify data files"
  shasum -c species/${SPEC}/checksums.sha
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
  echo "[HymHub: $FULLSPEC] clean up temporary files"
  find $WD -type f \
      | grep -v "/checksums.sha$" | grep -v "/data.sh$" \
      | grep -v "/${SPEC}.gdna.fa$" | grep -v "/${SPEC}.gff3$" \
      | grep -v ".tsv$" \
      | xargs -n 1 rm -f || true
fi

echo "[HymHub: $FULLSPEC] complete!"
