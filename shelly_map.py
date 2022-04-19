#!/usr/bin/python
import subprocess
import sys
import re
import urllib.request
import json

if len(sys.argv) < 3:
    print("Usage: " + " ".join(sys.argv) + " <network/prefix> <command>")
    print("%ip and %id in command get replaced")
    exit(1)

proc = subprocess.Popen(["nmap", "-p", "80", sys.argv[1]], stdout=subprocess.PIPE)
map = proc.stdout.read().decode().split("\n")
if proc.returncode != 0 and proc.returncode is not None:
    print(map)
    print(f"nmap exited with error code {proc.returncode}")
    exit(1)

shellies = []

def do_request(path):
    try:
        with urllib.request.urlopen(path) as response:
            if response.status != 200:
                return None
            return response.read().decode()
    except:
        return None

for i, item in enumerate(map):
    if "open" in item:
        ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', map[i - 4])
        if len(ips) != 1:
            continue
        ip = ips[0]

        shelly_resp = do_request(f"http://{ip}/shelly")
        if shelly_resp is None:
            continue

        settings_resp = do_request(f"http://{ip}/settings")
        if settings_resp is None:
            continue
        body = json.loads(settings_resp)
        shellies.append({
            "ip": ip,
            "id": body["device"]["hostname"]
        })

cmd = " ".join(sys.argv[2:])
for shelly in shellies:
    shelly_cmd = cmd.replace("%id", shelly["id"]).replace("%ip", shelly["ip"])
    subprocess.call(["sh", "-c", shelly_cmd])
