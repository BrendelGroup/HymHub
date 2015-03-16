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
      | python scripts/namedup.py \
      | $filtercmd \
      | grep -v $'\tregion\t' \
      | tidygff3 2> ${gff3}.tidy.log \
      | seq-reg.py - species/${SPEC}/${SPEC}.gdna.fa \
      | gt gff3 -sort -tidy -o ${gff3} -force 2>&1 \
      | grep -v 'has not been previously introduced' \
      | grep -v 'does not begin with "##gff-version"' || true

  echo "[HymHub: $FULLSPEC] verify data files"
  shasum -c species/${SPEC}/checksums.sha
}

hymbase_format_gtf()
{
  echo "[HymHub: $FULLSPEC] convert GTF to GFF3"
  filtercmd=cat
  if [ -n "$1" ]; then
    filtercmd="grep -Ev $1"
  fi
  mv $refrgff3 $refrgff3.orig
  gunzip -c $refrgff3.orig \
      | $filtercmd \
      | grep -v -e $'\tgene\t' -e $'\tmRNA\t' \
      | gt gtf_to_gff3 \
      | perl -ne 's/;gene_id=[^;\n]+;transcript_id=[^;\n]+//; print' \
      | perl -ne 's/(transcript_id=[^;\n]+);gene_id=[^;\n]+/$1/; print' \
      | sed 's/gene_id/Name/' \
      | sed 's/transcript_id/Name/' \
      | gt gff3 -sort -tidy -o >(gzip -c - > $refrgff3) -force 2>&1 \
      | grep -v 'wrong phase' || true

  hymbase_format
}
