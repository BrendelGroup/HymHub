# Copyright (c) 2015, Daniel S. Standage and CONTRIBUTORS
#
# HymHub is distributed under the CC BY 4.0 License. See the
# 'LICENSE' file in the HymHub code distribution or online at
# https://github.com/BrendelGroup/HymHub/blob/master/LICENSE.

data_print_usage()
{
  cat <<EOF
Usage: $0 [-w workdir] [-d] [-f] [-t] [-s] [-c] [-h]
  Options:
    -h    print this help message and exit
    -d    run download task (fetch raw data from primary sources)
    -f    run format task (streamline all data into a consistent format)
    -t    run datatypes task (extract features of interest and their sequences)
    -s    run statistics task (compute statistics on various features)
    -c    run cleanup task (remove intermediate data files)
    -w    working directory; default is current directory
EOF
}

WD="."
DODOWNLOAD=0
DOFORMAT=0
DODATATYPES=0
DOSTATS=0
DOCLEANUP=0
while getopts "cdfhstw:" OPTION
do
  case $OPTION in
    h) data_print_usage; exit 0 ;;
    d) DODOWNLOAD=1 ;;
    f) DOFORMAT=1 ;;
    t) DODATATYPES=1 ;;
    s) DOSTATS=1 ;;
    c) DOCLEANUP=1 ;;
    w) WD=$OPTARG ;;
  esac
done

if [ "$DODOWNLOAD"  == "0" ] && [ "$DOFORMAT"  == "0" ] &&
   [ "$DODATATYPES" == "0" ] && [ "$DOSTATS"   == "0" ] &&
   [ "$DOCLEANUP"   == "0" ]
then
  data_print_usage
  echo "Error: please specify task(s)"
  exit 1
fi
