#!/bin/bash

# set omd environment
export THRUK_CONFIG="/srv/eyesofnetwork/thruk"

# execute fastcgi server
exec /srv/eyesofnetwork/thruk/script/thruk_fastcgi.pl
