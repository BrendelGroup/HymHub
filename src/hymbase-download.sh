# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

# Procedure for downloading genomes and corresponding annotations for
# data sets from HymenopteraBase.
HYMBASE=http://hymenopteragenome.org/drupal/sites/hymenopteragenome.org.${URLGENUS}/files/data
hymbase_download()
{
  echo "[HymHub: $FULLSPEC] download genome from HymenopteraBase"
  curl ${HYMBASE}/${ORIGFASTA} > $refrfasta 2> ${refrfasta}.log

  echo "[HymHub: $FULLSPEC] download annotation from HymenopteraBase"
  curl ${HYMBASE}/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
}
