# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

# Fasta/GFF3 cleanup procedure for data sets obtained from HymenopteraBase.
hymbase_format()
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
      | python scripts/uniq.py \
      | $filtercmd \
      | grep -v $'\tregion\t' \
      | tidygff3 2> ${gff3}.tidy.log \
      | seq-reg.py - species/${SPEC}/${SPEC}.gdna.fa \
      | gt gff3 -retainids -sort -tidy -o ${gff3} -force 2> ${gff3}.log

  echo "[HymHub: $FULLSPEC] verify data files"
  shasum -c species/${SPEC}/checksums.sha
}
