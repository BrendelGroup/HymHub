# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

for spec in Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas
do
  bash species/${spec}/data.sh -w species/${spec} -d -f -t -s -c
done

for feattype in iloci genereps mrnas cds
do
  cp species/Ador/${feattype}.tsv data/${feattype}.tsv
  for spec in Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas
  do
    tail -n +2 species/${spec}/${feattype}.tsv >> data/${feattype}.tsv
  done
done
shasum -c data/checksums.sha
