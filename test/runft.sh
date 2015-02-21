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
    --exons test/ftest-exons.gff3 test/ftest-exons.fa test/exons-pre-test.tsv \
    --introns test/ftest-introns.gff3 test/ftest-introns.fa test/introns-pre-test.tsv

python scripts/feature-desc.py \
    --iloci test/ftest-miloci.gff3 test/ftest-miloci.fa test/miloci-test.tsv

head -n 1 test/exons-pre-test.tsv > test/exons-test.tsv
grep 'NT_033778.3_19722259-19722625' test/exons-pre-test.tsv >> test/exons-test.tsv
grep 'NW_003798164.1_151172-151385' test/exons-pre-test.tsv >> test/exons-test.tsv
grep 'PdomSCFr1.2-0001_325761-325941' test/exons-pre-test.tsv >> test/exons-test.tsv

head -n 1 test/introns-pre-test.tsv > test/introns-test.tsv
grep 'NW_006263543.1_1250931-1251032' test/introns-pre-test.tsv >> test/introns-test.tsv
grep 'NC_007416.2_8179063-8179106' test/introns-pre-test.tsv >> test/introns-test.tsv
grep 'NC_007419.1_6956030-6957921' test/introns-pre-test.tsv >> test/introns-test.tsv

for ftype in iloci miloci genereps mrnas cds exons introns
do
  echo -n "[HymHub]     $ftype functional test..."
  diff -q test/ftest-${ftype}.tsv test/${ftype}-test.tsv
  echo "passed!"
done
echo "[HymHub] functional tests complete"
