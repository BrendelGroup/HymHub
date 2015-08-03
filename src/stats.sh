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
      --prnas ${PRFX}.ilocus.mrnas.gff3 ${PRFX}.pre-mrnas.fa ${PRFX}.pre-mrnas.tsv \
      --mrnas ${PRFX}.mrnas.gff3 ${PRFX}.mrnas.fa ${PRFX}.mrnas.tsv \
      --cds ${PRFX}.ilocus.mrnas.gff3 ${PRFX}.cds.fa ${PRFX}.cds.tsv \
      --exons ${PRFX}.ilocus.mrnas.gff3 ${PRFX}.exons.fa ${PRFX}.exons.tsv \
      --introns ${PRFX}.ilocus.mrnas.gff3 ${PRFX}.introns.fa ${PRFX}.introns.tsv
  python scripts/feature-desc.py --species ${SPEC} \
      --iloci ${PRFX}.miloci.gff3 ${PRFX}.miloci.fa ${PRFX}.miloci.tsv
}

aggregate_stats()
{
  for feattype in iloci miloci pre-mrnas mrnas cds exons introns
  do
    cp species/Acep/Acep.${feattype}.tsv data/${feattype}.tsv
    for spec in Ador Aech Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pbar Pdom Sinv Tcas
    do
      tail -n +2 species/${spec}/${spec}.${feattype}.tsv >> data/${feattype}.tsv
    done
  done
  shasum -c data/checksums.sha
}

aggregate_stats_source()
{
  for feattype in iloci miloci pre-mrnas mrnas cds exons introns
  do
    cp species/Acep/Acep.${feattype}.tsv data/${feattype}.tsv
    for spec in Amel Am32 Bter Cflo Cfhb Dmel Hsal Nvit Pdom Sinv Sihb
    do
      tail -n +2 species/${spec}/${spec}.${feattype}.tsv >> data/${feattype}.tsv
    done
  done
}
