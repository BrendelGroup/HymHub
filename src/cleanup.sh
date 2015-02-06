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
      | grep -v "/excludes.txt" \
      | xargs -n 1 rm -f || true
}
