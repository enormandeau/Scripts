#!/bin/bash

clear
echo "IMPORTANT"
find /home/labolb/Dropbox/Lab/project_checklists/ -iname "*.txt" | \
    parallel echo -e "\#\#\# {/.} \#\#\#" \; grep "\.\." {} | \
    grep -B 1 "*" | \
    grep -v "^--" | \
    perl -pe 's/\#\#\#/\n\#\#\#/'
echo

