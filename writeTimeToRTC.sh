[ -z $BASH ] && { exec bash "$0" "$@" || exit; }
#!/bin/bash
# file: wittyPi.sh
#
# Run this application to interactly configure your Witty Pi
#

# include utilities script in same directory
my_dir="`dirname \"$0\"`"
my_dir="`( cd \"$my_dir\" && pwd )`"
if [ -z "$my_dir" ] ; then
  exit 1
fi
. $my_dir/../wittypi/utilities.sh

if ! is_rtc_connected ; then
  echo ''
  log 'Seems Witty Pi board is not connected? Quitting...'
  echo ''
  exit
fi

system_to_rtc
