# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

cluster_proteins()
{
  local VERSION=$(cat VERSION)
  echo "[HymHub] computing homologous iLoci"
  mkdir -p scratch/
  if [ "$1" != "SKIP" ]; then
    rm -f data/Hym.prot.fa
    for species in Acep Ador Aech Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot \
                   Nvit Pbar Pdom Sinv Tcas
    do
      cat species/${species}/${species}.prot.fa >> data/Hym.prot.fa
    done
    cd-hit -i data/Hym.prot.fa -o data/hym-prot -M 0 \
           -T 1 -d 0 -c 0.50 -s 0.65 -p 1 -n 3 \
           -aL 0.75 -aS 0.85 \
           > data/cdhit.log 2>&1
  fi

  python scripts/hilocus-create.py --mint="HymHubHIL${VERSION}-%06d" \
                                   --outfile=data/hiloci.tsv \
                                   data/hym-prot.clstr \
                                   <(cat species/*/*.protein2ilocus.txt)

  for mode in rep six four
  do
    echo "[HymHub] computing Hymenoptera-conserved hiLoci ($mode)"
    scripts/hilocus-conserved.py --mode $mode data/hiloci.tsv \
        > data/hiloci-conserved-${mode}.tsv 

    echo "[HymHub] extracting computed features for conserved hiLoci ($mode)"
    scripts/mrna-feat-subset.py -M 2 data/hiloci-conserved-${mode}.tsv \
        data/mrnas.tsv \
        > data/mrnas-hicons-${mode}.tsv
    for featuretype in exons introns cds
    do
      scripts/mrna-feat-subset.py \
          data/hiloci-conserved-${mode}.tsv \
          data/${featuretype}.tsv \
          > data/${featuretype}-hicons-${mode}.tsv
    done
  done

  echo "[HymHub] computing representative quartets of conserved hiLoci"
  scripts/hilocus-quartets.py data/hiloci-conserved-four.tsv \
      > data/quartets.tsv

  echo "[HymHub] computing breakdowns of genome content"
  scripts/genome-breakdown.py data/iloci.tsv data/hiloci.tsv \
                           data/hiloci-conserved-six.tsv \
      > data/breakdown-bp.tsv
  scripts/genome-breakdown.py --counts data/iloci.tsv data/hiloci.tsv \
                           data/hiloci-conserved-six.tsv \
      > data/breakdown-counts.tsv
  scripts/genome-breakdown.py --table data/iloci.tsv data/hiloci.tsv \
                           data/hiloci-conserved-six.tsv \
      > data/breakdown-iloci.temp
  scripts/add-utrs.py data/pre-mrnas.tsv data/breakdown-iloci.temp \
      > data/breakdown-iloci.tsv

  #shasum -c data/hilocus-data.sha
}
