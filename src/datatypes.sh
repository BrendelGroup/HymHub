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
              --ilenfile ${WD}/${SPEC}.ilens.txt \
              --out ${WD}/${SPEC}.iloci.gff3 \
              ${WD}/${SPEC}.gff3 \
      2> ${WD}/iloci.gff3.log
  python scripts/filens.py < ${WD}/${SPEC}.iloci.gff3 > ${WD}/${SPEC}.filens.tsv

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
  grep $'\tlocus\t' ${WD}/${SPEC}.iloci.gff3 \
      | grep 'mRNA=' \
      | grep 'gene=1;' \
      | perl -ne 'm/ID=([^;\n]+)/ and print "$1\n"' \
      > ${WD}/${SPEC}.simple-iloci.txt

  echo "[HymHub: ${SPEC}] identifying iLocus representatives (longest isoforms)"
  grep -v $'\tintron\t' ${WD}/${SPEC}.iloci.gff3 \
      | pmrna --locus --accession --map ${WD}/${SPEC}.ilocus.mrnas.txt \
      | canon-gff3 --outfile ${WD}/${SPEC}.ilocus.mrnas.gff3 2>&1 \
      | grep -v 'no valid mRNAs' || true
  cut -f 2 ${WD}/${SPEC}.ilocus.mrnas.txt > ${WD}/${SPEC}.mrnas.txt
}

get_genes()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting gene sequences"
  xtractore --type=gene ${WD}/${SPEC}.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.all.genes.fa

  echo "[HymHub: ${SPEC}] identifying gene representatives (longest isoforms)"
  grep -v $'\tintron\t' ${WD}/${SPEC}.gff3 \
      | pmrna --accession --map ${WD}/${SPEC}.mrna2gene.txt \
      | canon-gff3 --outfile ${WD}/${SPEC}.gene.mrnas.gff3 2>&1 \
      | grep -v 'no valid mRNAs' || true
  cut -f 2 ${WD}/${SPEC}.mrna2gene.txt > ${WD}/${SPEC}.gene.mrnas.txt
}

get_proteins()
{
  local SPEC=$1
  local WD=species/${SPEC}
  local specmode=$MODE
  if [ "$specmode" == "" ]; then
    specmode="ncbi"
  fi

  echo "[HymHub: ${SPEC}] extracting protein sequences"
  if [ "$specmode" == "hymbase" ]; then
    grep $'\tmRNA\t' ${WD}/${SPEC}.ilocus.mrnas.gff3 \
        | perl -ne 'm/Name=([^;\n]++)/ and print "$1\n"' \
        | perl -ne 's/-R/-P/; print' \
        | sort | uniq \
        > ${WD}/${SPEC}.protids.txt
  else
    grep $'\tCDS\t' ${WD}/${SPEC}.ilocus.mrnas.gff3 \
        | perl -ne 'm/protein_id=([^;\n]++)/ and print "$1\n"' \
        | sort | uniq \
        > ${WD}/${SPEC}.protids.txt
  fi
  python scripts/protein-ilocus-mapping.py --mode $specmode \
      ${WD}/${SPEC}.iloci.gff3 \
      > ${WD}/${SPEC}.protein2ilocus.txt
  python scripts/select-seq.py ${WD}/${SPEC}.protids.txt $protfa \
      | sed "s/>/>gnl|$SPEC|/" \
      > ${WD}/${SPEC}.prot.fa
}

get_mmrnas()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting pre-mRNA sequences"
  xtractore --type=mRNA ${WD}/${SPEC}.gff3 ${WD}/${SPEC}.gdna.fa \
      > ${WD}/${SPEC}.all.pre-mrnas.fa

  echo "[HymHub: ${SPEC}] extracting mature mRNA sequences"
  python scripts/mrna-exons.py --convert \
      < ${WD}/${SPEC}.gff3 \
      > ${WD}/${SPEC}.mrnas.temp
  gt gff3 -retainids -sort -tidy -force -o ${WD}/${SPEC}.all.mrnas.gff3 \
          ${WD}/${SPEC}.mrnas.temp 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
  xtractore --type=mRNA --outfile=${WD}/${SPEC}.all.mrnas.fa \
            ${WD}/${SPEC}.all.mrnas.gff3 ${WD}/${SPEC}.gdna.fa

  python scripts/mrna-exons.py --convert \
      < ${WD}/${SPEC}.ilocus.mrnas.gff3 \
      > ${WD}/${SPEC}.mrnas.temp
  gt gff3 -retainids -sort -tidy -force -o ${WD}/${SPEC}.mrnas.gff3 \
          ${WD}/${SPEC}.mrnas.temp 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true

  echo "[HymHub: ${SPEC}] selecting representative mRNAs"
  python scripts/select-seq.py ${WD}/${SPEC}.mrnas.txt ${WD}/${SPEC}.all.pre-mrnas.fa > ${WD}/${SPEC}.pre-mrnas.fa
  python scripts/select-seq.py ${WD}/${SPEC}.gene.mrnas.txt ${WD}/${SPEC}.all.pre-mrnas.fa > ${WD}/${SPEC}.gene.pre-mrnas.fa
  python scripts/select-seq.py ${WD}/${SPEC}.mrnas.txt ${WD}/${SPEC}.all.mrnas.fa > ${WD}/${SPEC}.mrnas.fa
  python scripts/select-seq.py ${WD}/${SPEC}.gene.mrnas.txt ${WD}/${SPEC}.all.mrnas.fa > ${WD}/${SPEC}.gene.mrnas.fa
}

get_cds()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting coding sequences"
  xtractore --type=CDS --outfile=${WD}/${SPEC}.all.cds.fa \
            ${WD}/${SPEC}.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
  xtractore --type=CDS --outfile=${WD}/${SPEC}.cds.fa \
            ${WD}/${SPEC}.ilocus.mrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
}

get_exons()
{
  local SPEC=$1
  local WD=species/${SPEC}

  echo "[HymHub: ${SPEC}] extracting exons"
  xtractore --type=exon --outfile=${WD}/${SPEC}.exons.fa \
            ${WD}/${SPEC}.ilocus.mrnas.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true

  echo "[HymHub: ${SPEC}] extracting introns"
  canon-gff3 ${WD}/${SPEC}.ilocus.mrnas.gff3 \
      | python scripts/intron-accessions.py \
      > ${WD}/${SPEC}-withintrons.gff3
  xtractore --type=intron --outfile=${WD}/${SPEC}.introns.fa \
            ${WD}/${SPEC}-withintrons.gff3 ${WD}/${SPEC}.gdna.fa 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true
  #rm ${WD}/${SPEC}-withintrons.gff3
}

get_datatypes()
{
  VERSION=$(cat VERSION)
  get_iloci    $1 $VERSION
  get_genes    $1
  get_proteins $1
  get_mmrnas   $1
  get_cds      $1
  get_exons    $1
}
