#!/usr/bin/env bash
# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

prep_workdir()
{
  local WD=$1
  if [ -e $WD ]; then
    >&2 echo -n "file/directory '$WD' exists; "
    >&2 echo "please specify a different working directory"
    exit 1
  fi
  mkdir $WD
}

prep_specdirs()
{
  local WD=$1

  for spec in $species
  do
    mkdir $WD/$spec
    cp species/$spec/${spec}.iloci.gff3 $WD/${spec}/.
    cp species/$spec/${spec}.iloci.fa $WD/${spec}/.
    cp species/$spec/${spec}*.tsv $WD/${spec}/.
  done
}

prep_datadir()
{
  local WD=$1
  mkdir $WD/summary-stats
  cp data/iloci.tsv data/miloci.tsv data/pre-mrnas.tsv $WD/summary-stats/.
  for feat in introns exons cds mrnas
  do
    cp data/${feat}.tsv $WD/summary-stats/.
    cp data/${feat}-hicons-rep.tsv $WD/summary-stats/.
    cp data/${feat}-hicons-four.tsv $WD/summary-stats/.
    cp data/${feat}-hicons-six.tsv $WD/summary-stats/.
  done
  cp data/hiloci-conserved-four.tsv \
     data/hiloci-conserved-six.tsv \
     data/hiloci-conserved-rep.tsv \
     data/hiloci.tsv \
     $WD/summary-stats/.
  cp data/breakdown-bp.tsv \
     data/breakdown-counts.tsv \
     data/breakdown-iloci.tsv \
     $WD/summary-stats/.
}

compress_dirs()
{
  local WD=$1
  local SPECS=$2

  cd $WD
  echo $SPECS summary-stats | tr ' ' '\n' | parallel --gnu tar cjf {}.tar.bz2 {}
  cd - > /dev/null 2>&1
}

# Main method
#-------------------------------------------------------------------------------
species="Acep Ador Aech Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pbar Pdom Sinv Tcas"
prep_workdir  $1
prep_specdirs $1
prep_datadir  $1
compress_dirs $1 "$species"
