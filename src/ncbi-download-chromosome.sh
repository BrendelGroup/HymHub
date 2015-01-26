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
