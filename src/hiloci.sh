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
  cat species/*/*.rep-prot.fa > scratch/Hym.rep-prot.fa
  if [ "$1" != "SKIP" ]; then
    cd-hit -i scratch/Hym.rep-prot.fa -o data/hym-prot -M 0 \
           -T 1 -d 0 -c 0.50 -s 0.65 -p 1 -n 3 \
           -aL 0.75 -aS 0.85 \
           > scratch/cdhit.log 2>&1
  fi

  python scripts/hilocus-create.py --mint="HymHubHIL${VERSION}-%06d" \
                                   --outfile=data/hiloci.tsv \
                                   data/hym-prot.clstr \
                                   <(cat species/*/*.protein2ilocus.txt)

  echo "[HymHub] computing Hymenoptera-conserved quartets"
  scripts/hilocus-quartets.py data/hiloci.tsv > data/quartets.tsv

  echo "[HymHub] extracting hiLocus mRNA representatives"
  scripts/mrna-rep-summ.sh
  for featuretype in exons introns cds
  do
    scripts/mrna-feat-subset.py data/${featuretype}.tsv \
        > data/${featuretype}-hirep.tsv
  done

  shasum -c data/hilocus-data.sha
}
