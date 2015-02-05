#!/usr/bin/env bash
set -eo pipefail

for spec in Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas
do
  WD=species/${spec}
  grep -v '#' ${WD}/${spec}.gff3 | cut -f 1 | sort | uniq > ${WD}/gff3seqids
  perl -ne 'm/^>(\S+)/ and print "$1\n"' < ${WD}/${spec}.gdna.fa | sort > ${WD}/faseqids

  echo -e "\n\n${spec} IDs: GFF3 vs Fasta"

  echo -n "    In common: "
  comm -12 ${WD}/gff3seqids ${WD}/faseqids > ${WD}/comm12
  wc -l < ${WD}/comm12

  echo -n "    Fasta only: "
  comm -13 ${WD}/gff3seqids ${WD}/faseqids > ${WD}/comm13
  wc -l < ${WD}/comm13

  echo -n "    GFF3 only: "
  comm -23 ${WD}/gff3seqids ${WD}/faseqids > ${WD}/comm23
  wc -l < ${WD}/comm23
done
