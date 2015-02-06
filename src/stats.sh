# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

get_stats()
{
  local SPEC=$1
  local PRFX=species/${SPEC}/${SPEC}

  python scripts/feature-desc.py \
      --iloci ${PRFX}.iloci.gff3 ${PRFX}.iloci.fa ${PRFX}.iloci.tsv
}
