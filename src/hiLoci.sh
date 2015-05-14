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
  cd-hit -i scratch/Hym.rep-prot.fa -o data/hym-prot -M 0 \
         -T 1 -d 0 -c 0.65 -s 0.65 -p 1 -n 4 \
         > scratch/cdhit.log 2>&1

  python src/hilocus.py --mint="HymHubHIL${VERSION}-%06d" \
                        --outfile=data/hiloci.tsv \
                        data/hym-prot.clstr \
                        <(cat species/*/*.protein2ilocus.txt)
  shasum -c data/hiLoci.sha
}
