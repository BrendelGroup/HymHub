# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

get_stats()
{
  local SPEC=$1
  local PRFX=species/${SPEC}/${SPEC}

  echo "[HymHub: $SPEC] computing feature summary statistics"
  python scripts/feature-desc.py --species ${SPEC} \
      --iloci ${PRFX}.iloci.gff3 ${PRFX}.iloci.fa ${PRFX}.iloci.tsv \
      --gnreps ${PRFX}.pmrnas.gff3 ${PRFX}.genereps.fa ${PRFX}.genereps.tsv \
      --mrnas ${PRFX}.maturemrnas.gff3 ${PRFX}.maturemrnas.fa ${PRFX}.mrnas.tsv \
      --cds ${PRFX}.pmrnas.gff3 ${PRFX}.cds.fa ${PRFX}.cds.tsv \
      --exons ${PRFX}.pmrnas.gff3 ${PRFX}.exons.fa ${PRFX}.exons.tsv \
      --introns ${PRFX}.pmrnas.gff3 ${PRFX}.introns.fa ${PRFX}.introns.tsv
  python scripts/feature-desc.py --species ${SPEC} \
      --iloci ${PRFX}.miloci.gff3 ${PRFX}.miloci.fa ${PRFX}.miloci.tsv
}

aggregate_stats()
{
  for feattype in iloci miloci genereps mrnas cds exons introns
  do
    cp species/Ador/Ador.${feattype}.tsv data/${feattype}.tsv
    for spec in Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas
    do
      tail -n +2 species/${spec}/${spec}.${feattype}.tsv >> data/${feattype}.tsv
    done
  done
  shasum -c data/checksums.sha
}
