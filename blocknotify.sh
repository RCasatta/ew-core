#!/bin/sh

#curl "https://eternitywall.appspot.com/v1/hooks/rawblock?hash=$@" -d "CIAO"
#curl "https://eternitywall.appspot.com/v1/hooks/rawblock?hash=$@" -d "$@"
python /home/casatta/ew_extract.py $@
date >/home/casatta/notified


