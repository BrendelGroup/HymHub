#!/usr/bin/env bash
#
# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

mkdir -p scratch
scripts/hilocus-quartets.py data/hiloci.tsv > scratch/hilocus-reps-temp.txt

rm -f scratch/bees-mrnas-temp.tsv
for spec in Ador Aflo Amel Bimp Bter Mrot
do
  scripts/selex.pl -o 1 \
      <(grep $spec scratch/hilocus-reps-temp.txt | cut -f 2) \
      species/${spec}/${spec}.locus-pmrnas.txt \
      > scratch/${spec}-mrnas-temp.txt
  scripts/selex.pl -k 1 scratch/${spec}-mrnas-temp.txt \
      species/${spec}/${spec}.mrnas.tsv \
      >> scratch/bees-mrnas-temp.tsv
done

rm -f scratch/ants-mrnas-temp.tsv
for spec in Acep Aech Cflo Hsal Pbar Sinv
do
  scripts/selex.pl -o 1 \
      <(grep $spec scratch/hilocus-reps-temp.txt | cut -f 2) \
      species/${spec}/${spec}.locus-pmrnas.txt \
      > scratch/${spec}-mrnas-temp.txt
  scripts/selex.pl -k 1 scratch/${spec}-mrnas-temp.txt \
      species/${spec}/${spec}.mrnas.tsv \
      >> scratch/ants-mrnas-temp.tsv
done

for spec in Nvit Pdom
do
  scripts/selex.pl -o 1 \
      <(grep $spec scratch/hilocus-reps-temp.txt | cut -f 2) \
      species/${spec}/${spec}.locus-pmrnas.txt \
      > scratch/${spec}-mrnas-temp.txt
  scripts/selex.pl -k 1 scratch/${spec}-mrnas-temp.txt \
      species/${spec}/${spec}.mrnas.tsv \
      > scratch/${spec}-mrnas-temp.tsv
done

head -n 1 species/Amel/Amel.mrnas.tsv > data/hilocus-reps.tsv
cat scratch/*-mrnas-temp.tsv >> data/hilocus-reps.tsv
