#!/usr/bin/python

import subprocess, json
from datetime import datetime as dt

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
print sys.path

from sensor_db import Db
db = Db()

fname = "lan_status.txt"
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

cmd = "sudo nmap -sn 192.168.1.0-150"
rs = subprocess.check_output(cmd, shell=True)

lines = rs.split("\n")

count = 0
macs = {}

for line in lines[2:]:
    print line
    pieces = line.split("MAC Address: ")
    if len(pieces) == 2:
        mac = pieces[1].split(" ")[0]
        macs.update({mac: True})

now = dt.now().strftime(ISO_FORMAT)
wils_mac = '90:B6:86:2B:14:D7'
if macs[wils_mac]:
    # db.create_device(wils_mac)
    db.update_device(wils_mac, 1)
