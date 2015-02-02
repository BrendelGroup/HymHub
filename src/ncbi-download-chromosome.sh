# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

# Procedure for downloading chromosome-based genomes and corresponding
# annotations for data sets from NCBI.
NCBIBASE=ftp://ftp.ncbi.nih.gov/genomes/$(echo $FULLSPEC | tr ' ' '_')
ncbi_download_chromosome()
{
  echo "[HymHub: $FULLSPEC] download genome from NCBI"
  rm -f ${refrfasta} ${refrfasta}.temp ${refrfasta}.log
  for file in $ASMBLFILES
  do
    curl ${NCBIBASE}/$file 2>> ${refrfasta}.log | gunzip -c >> ${refrfasta}.temp
  done
  gzip ${refrfasta}.temp
  mv ${refrfasta}.temp.gz $refrfasta

  echo "[HymHub: $FULLSPEC] download annotation from NCBI"
  curl ${NCBIBASE}/GFF/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
}
