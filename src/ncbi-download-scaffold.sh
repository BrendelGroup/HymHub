ncbi_download_scaffold()
{
  echo "[HymHub: $FULLSPEC] download genome from NCBI"
  curl ${NCBIBASE}/CHR_Un/${ORIGFASTA} > $refrfasta 2> ${refrfasta}.log

  echo "[HymHub: $FULLSPEC] download annotation from NCBI"
  curl ${NCBIBASE}/GFF/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
}
