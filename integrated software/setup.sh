#!/bin/sh
# intsall dependancies
sudo apt-get update
sudo apt-get upgrade
sudo pip3 install --upgrade setuptools

sudo pip3 install numpy
sudo apt-get install python3-scipy
sudo pip3 install RPi.GPIO
sudo pip3 install smbus # not sure if this will work
sudo pip3 install adafruit-circuitpython-mcp3xxx
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py