#!/bin/sh
python shelly_map.py $1 curl "%ip/relay/0?turn=$2"
