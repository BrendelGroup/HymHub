# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

data_cleanup()
{
  echo "[HymHub: $FULLSPEC] clean up temporary files"
  find $WD -type f \
      | grep -v "/checksums.sha$" | grep -v "/data.sh$" \
      | grep -v "/${SPEC}.gdna.fa$" | grep -v "/${SPEC}.gff3$" \
      | grep -v "/excludes.txt" | grep -v ".tsv$" \
      | grep -v ".py$" | grep -v ".sh$" | grep -v "/${SPEC}.rep-prot.fa" \
      | grep -v "/${SPEC}.protein2ilocus.txt" | grep -v "locus-pmrnas.txt" \
      | grep -v "ilocus.mrnas.txt" | grep -v 'simple-iloci.txt' \
      | xargs -n 1 rm -f || true
}
