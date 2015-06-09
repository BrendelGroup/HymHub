# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail
source src/stats.sh
source src/hiloci.sh

if [ -f data/hym-prot.clstr.bz2 ]; then
  bunzip2 data/hym-prot.clstr.bz2
fi
test -f data/hym-prot.clstr
test/runft.sh
for spec in Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas
do
  bash species/${spec}/data.sh -w species/${spec} -d -f -t -s -c
done
aggregate_stats
cluster_proteins SKIP
