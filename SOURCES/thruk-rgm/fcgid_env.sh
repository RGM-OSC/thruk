#!/bin/bash

# set omd environment
export THRUK_CONFIG="/srv/rgm/thruk"

# execute fastcgi server
exec /srv/rgm/thruk/script/thruk_fastcgi.pl
