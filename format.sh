# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

format_print_usage()
{
  cat <<EOF
Usage: $0 [-p NUMTHREADS] [-c] [-h]
  Options:
    -h    print this help message and exit
    -p    run tasks in parallel (using GNU parallel program)
    -c    run cleanup task
EOF
}

NUMTHREADS=1
DOCLEANUP=0
while getopts "chp:" OPTION
do
  case $OPTION in
    h) format_print_usage; exit 0 ;;
    c) DOCLEANUP=1 ;;
    p) NUMTHREADS=$OPTARG ;;
  esac
done

SPECIES="Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas"

if [ $NUMTHREADS > 1 ]; then
  cmd="bash species/{}/data.sh -w species/{} -f"
  if [ "$DOCLEANUP" != "0" ]; then
    cmd="$cmd -c"
  fi
  echo $SPECIES | tr ' ' '\n' | parallel --gnu --jobs $NUMTHREADS $cmd
else
  for spec in $SPECIES
  do
    cmd="bash species/${spec}/data.sh -w species/${spec} -f"
    if [ "$DOCLEANUP" != "0" ]; then
      cmd="$cmd -c"
    fi
    $cmd
  done
fi
