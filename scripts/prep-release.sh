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

  cp -r species/* $WD/.
  rm -f $WD/*/*.gz $WD/*/*.log $WD/*/*.temp $WD/*/data.sh $WD/*/excludes.txt \
        $WD/*/*.py $WD/*/N?_??????.*
  ls $WD/*/*.fa | grep -v '.gdna.fa' | grep -v '.iloci.fa' | xargs rm
}

prep_datadir()
{
  local WD=$1
  cp -r data $WD/summary-stats
  rm $WD/summary-stats/HymHubDemo*
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
