#!/bin/bash

# Keep a file with ALL commands ever used in history, unique and sorted
cat ~/.bash_history ~/my_bash_history.txt >~/temp_my_bash_history
sort -u ~/temp_my_bash_history > ~/my_bash_history.txt
rm ~/temp_my_bash_history
