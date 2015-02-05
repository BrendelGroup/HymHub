# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

get_iloci()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] computing iLocus boundaries"
  lpdriver.py --idfmt="HymHub${SPEC}ILCv0.0.1-%05lu" --delta=500 \
              --out ${WD}/${SPEC}.iloci.gff3 \
              ${WD}/${SPEC}.gff3 \
      2> ${WD}/iloci.gff3.log

  echo "[HymHub: ${SPEC}] extracting iLocus sequences"
  xtractore --type=locus ${WD}/${SPEC}.iloci.gff3 \
            ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.iloci.fa
}

get_genes()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting gene sequences"
  xtractore --type=gene ${WD}/${SPEC}.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.genes.fa

  echo "[HymHub: ${SPEC}] extracting gene representatives (longest isoforms)"
  xtractore --type=mRNA <(grep -v $'\tintron\t' ${WD}/${SPEC}.gff3 | pmrna) \
                        ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.genereps.fa
  perl -ne 'm/^>(\S+)/ and print "$1\n"' \
      < ${WD}/${SPEC}.genereps.fa \
      > ${WD}/${SPEC}.generepids.txt
}

get_datatypes()
{
  get_iloci $1
  get_genes $1
}

