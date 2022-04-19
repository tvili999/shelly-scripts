#!/bin/sh
python shelly_map.py $1 curl "%ip/settings/relay/0?default_state=$2"

