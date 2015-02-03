# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail
source src/datatypes.sh

for spec in Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Sinv Tcas
do
  bash species/${spec}/data.sh -w species/${spec} -d -f -c
  bash src/datatypes.sh $spec
done
