#!/bin/sh
sudo apt-get
sudo apt-get update && sudo apt-get upgrade -y
sudo apt install python3 python3-pip
sudo python -m pip install --upgrade pip setuptools virtualenv
sudo python -m pip install -r requirements.txt