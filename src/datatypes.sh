# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

get_iloci()
{
  echo "[HymHub: ${1}] computing iLocus boundaries"
  lpdriver.py --idfmt="HymHub${1}ILCv0.0.1-%05lu" --delta=500 \
              --out species/${1}/${1}.iloci.gff3 \
              species/${1}/${1}.gff3 \
      2> species/${1}/iloci.gff3.log

  echo "[HymHub: ${1}] extracting iLocus sequences"
  xtractore --type=locus species/${1}/${1}.iloci.gff3 \
            species/${1}/${1}.gdna.fa \
      > species/${1}/${1}.iloci.fa
}

if [ -n "$1" ]; then
  get_iloci $1
fi
