# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

get_iloci()
{
  local SPEC=$1
  local VERSION=$2
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] computing iLocus boundaries"
  lpdriver.py --idfmt="HymHub${SPEC}ILC${VERSION}-%05lu" --delta=500 \
              --out ${WD}/${SPEC}.iloci.gff3 \
              ${WD}/${SPEC}.gff3 \
      2> ${WD}/iloci.gff3.log

  echo "[HymHub: ${SPEC}] merging iLoci"
  miloci.py < ${WD}/${SPEC}.iloci.gff3 > ${WD}/${SPEC}.miloci.gff3

  echo "[HymHub: ${SPEC}] extracting iLocus sequences"
  xtractore --type=locus ${WD}/${SPEC}.iloci.gff3 \
            ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.iloci.fa
  xtractore --type=locus ${WD}/${SPEC}.miloci.gff3 \
            ${WD}/${SPEC}.gdna.fa \
      3>&1 1>&2 2>&3 > ${WD}/${SPEC}.miloci.fa \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
}

get_genes()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting gene sequences"
  xtractore --type=gene ${WD}/${SPEC}.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.genes.fa

  echo "[HymHub: ${SPEC}] extracting gene representatives (longest isoforms)"
  grep -v $'\tintron\t' ${WD}/${SPEC}.gff3 | pmrna \
      | canon-gff3 --outfile ${WD}/${SPEC}.pmrnas.gff3 2>&1 \
      | grep -v 'no valid mRNAs' || true
  xtractore --type=mRNA ${WD}/${SPEC}.pmrnas.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.genereps.fa
  perl -ne 'm/^>(\S+)/ and print "$1\n"' \
      < ${WD}/${SPEC}.genereps.fa \
      > ${WD}/${SPEC}.generepids.txt
}

get_proteins()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting protein sequences"
  grep $'\tCDS\t' ${WD}/${SPEC}.pmrnas.gff3 \
      | perl -ne 'm/protein_id=([^;\n]++)/ and print "$1\n"' \
      | sort | uniq \
      > ${WD}/${SPEC}.protids.txt
  perl scripts/select-seq.py ${WD}/${SPEC}.protids.txt $protfa \
      > ${WD}/${SPEC}.rep-prot.fa
  python scripts/protein-ilocus-mapping.py < ${WD}/${SPEC}.iloci.gff3 \
      > ${WD}/${SPEC}.protein2ilocus.txt
}

get_mmrnas()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting mature mRNA sequences"
  python scripts/mrna-exons.py --convert \
      < ${WD}/${SPEC}.pmrnas.gff3 \
      > ${WD}/${SPEC}.maturemrnas.temp
  gt gff3 -retainids -sort -tidy -force -o ${WD}/${SPEC}.maturemrnas.gff3 \
          ${WD}/${SPEC}.maturemrnas.temp 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
  xtractore --type=mRNA --outfile=${WD}/${SPEC}.maturemrnas.fa \
            ${WD}/${SPEC}.maturemrnas.gff3 ${WD}/${SPEC}.gdna.fa
}

get_cds()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting coding sequences"
  xtractore --type=CDS --outfile=${WD}/${SPEC}.cds.fa \
            ${WD}/${SPEC}.pmrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
}

get_exons()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting exons"
  xtractore --type=exon --outfile=${WD}/${SPEC}.exons.fa \
            ${WD}/${SPEC}.pmrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true

  echo "[HymHub: ${SPEC}] extracting introns"
  xtractore --type=intron --outfile=${WD}/${SPEC}.introns.fa \
            ${WD}/${SPEC}.pmrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
}

get_datatypes()
{
  VERSION=$(cat VERSION)
  #get_iloci    $1 $VERSION
  get_genes    $1
  get_proteins $1
  #get_mmrnas   $1
  #get_cds      $1
  #get_exons    $1
}
