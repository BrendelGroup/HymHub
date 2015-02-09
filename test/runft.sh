# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

echo "[HymHub] running functional tests"
python scripts/feature-desc.py \
    --iloci test/ftest-iloci.gff3 test/ftest-iloci.fa test/iloci-test.tsv \
    --gnreps test/ftest-genereps.gff3 test/ftest-genereps.fa test/genereps-test.tsv

for ftype in iloci genereps
do
  echo -n "[HymHub]     $ftype functional test..."
  diff -q test/ftest-${ftype}.tsv test/${ftype}-test.tsv
  echo "passed!"
done
echo "[HymHub] functional tests complete"
