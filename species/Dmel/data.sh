#!/usr/bin/env bash
set -eo pipefail

# Contributed 2015
# Daniel Standage <daniel.standage@gmail.com>

# Configuration
#-------------------------------------------------------------------------------
FULLSPEC="Drosophila melanogaster"
SPEC=Dmel
ORIGFASTA=${SPEC}.orig.fa.gz
ORIGGFF3=dmel-5.48-ncbi.gff3.gz
WD=$1
NCBIBASE=ftp://ftp.ncbi.nih.gov/genomes/Drosophila_melanogaster/RELEASE_5_48

# Procedure
#-------------------------------------------------------------------------------
refrfasta=${WD}/${ORIGFASTA}
refrgff3=${WD}/${ORIGGFF3}
fasta=${WD}/${SPEC}.gdna.fa
gff3=${WD}/${SPEC}.gff3

echo "[HymHub: $FULLSPEC] download genome and annotations from NCBI"
for chr in CHR_X/NC_004354 /CHR_2/NT_033778 CHR_2/NT_033779 CHR_3/NT_033777 \
           CHR_3/NT_037436 CHR_4/NC_004353
do
  basename=$(basename $chr)
  curl ${NCBIBASE}/${chr}.fna > ${WD}/${basename}.fa 2> ${WD}/${basename}.fa.log
  curl ${NCBIBASE}/${chr}.gff > ${WD}/${basename}.gff 2> ${WD}/${basename}.gff.log
done
cat ${WD}/N*_*.fa | gzip -c > $refrfasta
gt gff3 -sort -tidy ${WD}/N*_*.gff 2> ${refrgff3}.log | gzip -c > $refrgff3

echo "[HymHub: $FULLSPEC] simplify genome Fasta deflines"
gunzip -c $refrfasta \
    | perl -ne 's/gi\|\d+\|(ref|gb)\|([^\|]+)\S+/$2/; print' \
    > $fasta

echo "[HymHub: $FULLSPEC] clean up annotation"
gunzip -c $refrgff3 \
    | grep -v -f species/Dmel/excludes.txt \
    | species/Dmel/fix-trna.py \
    | tidy 2> ${gff3}.tidy.log \
    | gt gff3 -retainids -sort -tidy -o ${gff3} -force 2> ${gff3}.log

echo "[HymHub: $FULLSPEC] complete!"

