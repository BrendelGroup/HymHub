HYMBASE=http://hymenopteragenome.org/drupal/sites/hymenopteragenome.org.${URLGENUS}/files/data

hymbase_download()
{
  echo "[HymHub: $FULLSPEC] download genome from HymenopteraBase"
  curl ${HYMBASE}/${ORIGFASTA} > $refrfasta 2> ${refrfasta}.log

  echo "[HymHub: $FULLSPEC] download annotation from HymenopteraBase"
  curl ${HYMBASE}/${ORIGGFF3} > $refrgff3 2> ${refrgff3}.log
}
