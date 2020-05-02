#!/bin/bash

pip3 install gym

cd ..
git clone git@github.com:keras-rl/keras-rl.git
cd keras-rl/
ls
sudo python3 setup.py install

