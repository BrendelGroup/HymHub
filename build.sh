# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.
set -eo pipefail

build_print_usage()
{
  cat <<EOF
build.sh: Build HymHub data files

Usage: $0 [-d] [-f] [-t] [-s] [-c] [-h] [-i] [-p NUMTHREADS]
  Tasks:
    -d    run download task (fetch raw data from primary sources)
    -f    run format task (streamline all data into a consistent format)
    -t    run datatypes task (extract features of interest and their sequences)
    -s    run statistics task (compute statistics on various features)
    -c    run cleanup task (remove intermediate data files
  Options:
    -h    print this help message and exit
    -p    run tasks in parallel (using GNU parallel program)
EOF
}

DODOWNLOAD=0
DOFORMAT=0
DODATATYPES=0
DOSTATS=0
DOCLEANUP=0
NUMTHREADS=1
while getopts "cdfhp:st" OPTION
do
  case $OPTION in
    d) DODOWNLOAD=1 ;;
    f) DOFORMAT=1 ;;
    t) DODATATYPES=1 ;;
    s) DOSTATS=1 ;;
    c) DOCLEANUP=1 ;;
    h) build_print_usage; exit 0 ;;
    p) NUMTHREADS=$OPTARG ;;
  esac
done
shift $((OPTIND-1))

if [ "$DODOWNLOAD"  == "0" ] && [ "$DOFORMAT"  == "0" ] &&
   [ "$DODATATYPES" == "0" ] && [ "$DOSTATS"   == "0" ] &&
   [ "$DOCLEANUP"   == "0" ]
then
  build_print_usage
  echo "Error: please specify build task(s)"
  exit 1
fi
tasks=""
if [ "$DOFORMAT" == "1" ]; then
  tasks+=" -f"
fi
if [ "$DOCLEANUP" == "1" ]; then
  tasks+=" -c"
fi
if [ "$DODATATYPES" == "1" ]; then
  tasks+=" -t"
fi
if [ "$DOSTATS" == "1" ]; then
  tasks+=" -s"
fi

SPECIES="Ador Aflo Amel Bimp Bter Cflo Dmel Hsal Mrot Nvit Pdom Sinv Tcas"
if [ "$NUMTHREADS" -gt "1" ]; then
  if [ "$DODOWNLOAD" == "1" ]; then
    # Even in parallel mode, data files should be downloaded one at a time
    for spec in $SPECIES
    do
      bash species/${spec}/data.sh -w species/${spec} -d
    done
  fi

  # Run format/cleanup/datatype tasks in parallel
  if [ -n "$tasks" ]; then
    echo $SPECIES | tr ' ' '\n' | parallel --gnu --jobs $NUMTHREADS \
        bash species/{}/data.sh -w species/{} $tasks
  fi
else
  if [ "$DODOWNLOAD" == "1" ]; then
    tasks+=" -d"
  fi
  for spec in $SPECIES
  do
    if [ -n "$tasks" ]; then
      bash species/${spec}/data.sh -w species/${spec} $tasks
    fi
  done
fi

if [ "$DOSTATS" == "1" ]; then
  cp species/Ador/Ador.iloci.tsv data/iloci.tsv
  for spec in $SPECES
  do
    tail -n +2 species/${spec}/${spec}.iloci.tsv >> data/iloci.tsv
  done
  shasum -c data/checksums.sha
fi
