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
  grep -v $'\tintron\t' ${WD}/${SPEC}.gff3 | pmrna > ${WD}/${SPEC}.pmrnas.gff3
  xtractore --type=mRNA ${WD}/${SPEC}.pmrnas.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.genereps.fa
  perl -ne 'm/^>(\S+)/ and print "$1\n"' \
      < ${WD}/${SPEC}.genereps.fa \
      > ${WD}/${SPEC}.generepids.txt
}

get_mmrnas()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting mature mRNA sequences"
  python scripts/mrna-exons.py --convert \
      < ${WD}/${SPEC}.pmrnas.gff3 \
      > ${WD}/${SPEC}.maturemrnas.gff3
  xtractore --type=mRNA --outfile=${WD}/${SPEC}.maturemrnas.fa \
            ${WD}/${SPEC}.maturemrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
}

get_datatypes()
{
  get_iloci  $1
  get_genes  $1
  get_mmrnas $1
}

