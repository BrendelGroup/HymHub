hymbase_cleanup()
{
  echo "[HymHub: $FULLSPEC] simplify genome Fasta deflines"
  gunzip -c $refrfasta \
      | perl -ne 's/gnl\|[^|]+\|//g; print' \
      > $fasta

  filtercmd=cat
  if [ -n "$1" ]; then
    filtercmd="grep -Ev $1"
  fi
  echo "[HymHub: $FULLSPEC] clean up annotation"
  gunzip -c $refrgff3 \
      | $filtercmd \
      | tidy 2> ${gff3}.tidy.log \
      | gt gff3 -retainids -sort -tidy -o ${gff3} -force 2> ${gff3}.log
}
