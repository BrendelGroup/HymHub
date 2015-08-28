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

  echo "[HymHub] computing Hymenoptera-conserved hiLoci"
  scripts/hilocus-conserved.py data/hiloci.tsv > data/hiloci-conserved.tsv 

  echo "[HymHub] computing representative quartets of conserved hiLoci"
  scripts/hilocus-quartets.py --seed 2466724 \
      data/hiloci-conserved.tsv \
      > data/quartets.tsv

  echo "[HymHub] extracting computed features for conserved hiLoci"
  scripts/mrna-feat-subset.py -M 2 data/hiloci-conserved.tsv \
      data/mrnas.tsv \
      > data/mrnas-hicons.tsv
  for featuretype in exons introns cds
  do
    scripts/mrna-feat-subset.py \
        data/hiloci-conserved.tsv \
        data/${featuretype}.tsv \
        > data/${featuretype}-hicons.tsv
  done

  #shasum -c data/hilocus-data.sha
}
