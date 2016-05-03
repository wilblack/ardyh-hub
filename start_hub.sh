#!/bin/bash
# This script runs the Ardyh Hub
# written by Wil Black wilblack21@gmail.com Feb. 4 2016


export PYTHONPATH=$PYTHONPATH:/home/pi/projects/RPi-LPD8806:/home/pi/projects/BrickPi_Python

cd  /home/pi/projects/lilybot/hub
#sudo chmod 755 RPi_Server_Code.py

echo "Killing and previous instances"
sudo kill $(ps -e | sudo netstat -tlnp | awk '/:9093 */ {split($NF,a,"/"); print a[1]}')

NOW=$(date +"%Y-%m-%dT%T %Z")
echo "[$NOW] Starting and ardyh hub"

modprobe i2c-bcm2708
modprobe i2c-dev

python main.py
