#!/bin/bash
# Fix wifi problem on lenovo thinkpad E431 laptop
sudo rmmod iwldvm 
sudo rmmod iwlwifi 
sudo modprobe iwlwifi 11n_disable=1
sudo modprobe iwlwifi
sudo modprobe iwldvm

