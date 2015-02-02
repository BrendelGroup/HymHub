# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

# Procedure for downloading scaffold-based genomes and corresponding
# annotations for data sets from NCBI.
NCBIBASE=ftp://ftp.ncbi.nih.gov/genomes/$(echo $FULLSPEC | tr ' ' '_')
ncbi_download_scaffold()
{
  echo "[HymHub: $FULLSPEC] download genome from NCBI"
  curl ${NCBIBASE}/CHR_Un/${ORIGFASTA} > $refrfasta 2> ${refrfasta}.log

  echo "[HymHub: $FULLSPEC] download annotation from NCBI"
  curl ${NCBIBASE}/GFF/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
}
