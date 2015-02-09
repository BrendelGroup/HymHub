# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

echo "[HymHub] running functional tests"
python scripts/feature-desc.py \
    --iloci test/ftest-iloci.gff3 test/ftest-iloci.fa test/iloci-test.tsv \
    --gnreps test/ftest-genereps.gff3 test/ftest-genereps.fa test/genereps-test.tsv \
    --mrnas test/ftest-mrnas.gff3 test/ftest-mrnas.fa test/mrnas-test.tsv \
    --cds test/ftest-cds.gff3 test/ftest-cds.fa test/cds-test.tsv \
    --exons test/ftest-exons.gff3 test/ftest-exons.fa test/exons-pre-test.tsv

head -n 1 test/exons-pre-test.tsv > test/exons-test.tsv
grep 'NT_033778.3_19722259-19722625' test/exons-pre-test.tsv >> test/exons-test.tsv
grep 'NW_003798164.1_151172-151385' test/exons-pre-test.tsv >> test/exons-test.tsv
grep 'PdomSCFr1.2-0001_325761-325941' test/exons-pre-test.tsv >> test/exons-test.tsv

for ftype in iloci genereps mrnas cds exons
do
  echo -n "[HymHub]     $ftype functional test..."
  diff -q test/ftest-${ftype}.tsv test/${ftype}-test.tsv
  echo "passed!"
done
echo "[HymHub] functional tests complete"
