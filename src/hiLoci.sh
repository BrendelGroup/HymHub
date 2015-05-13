# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

cluster_proteins()
{
  mkdir -p scratch/
  cat species/*/*.rep-prot.fa > scratch/Hym.rep-prot.fa
  cd-hit -i scratch/Hym.rep-prot.fa -o data/hym-prot -M 0 \
         -T 1 -d 0 -c 0.65 -s 0.65 -p 1 -n 4 \
         > scratch/cdhit.log 2>&1
  shasum data/hym-prot.clstr
  head -n 100 data/hym-prot.clstr
  shasum -c data/hiLoci.sha
}
