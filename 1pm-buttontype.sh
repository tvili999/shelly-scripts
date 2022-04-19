#!/bin/sh
python shelly_map.py $1 curl "%ip/settings/relay/0?btn_type=$2"

