#!/bin/bash
clear
echo "-=( IMPORTANT )=-"

find /home/labolb/Dropbox/Lab/project_checklists/ | \
    grep -v "~" | \
    while read i
    do
        
        echo "### $(echo $(basename $(echo $i) | perl -pe 's/\.txt//') | perl -ne 'print uc($_)') ###"
        grep "*" $i
    done | \
        grep -B 1 "*" | \
        grep -v "^--" | \
        perl -pe 's/^#/\n#/'

