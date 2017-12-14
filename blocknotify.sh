#!/bin/sh

#curl "https://eternitywall.appspot.com/v1/hooks/rawblock?hash=$@" -d "CIAO"
#curl "https://eternitywall.appspot.com/v1/hooks/rawblock?hash=$@" -d "$@"
python bin/ew_extract.py $@
