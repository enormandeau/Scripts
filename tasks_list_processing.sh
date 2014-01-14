#!/bin/bash
echo
echo "-=( PROCESSING )=-"

find /home/labolb/Dropbox/Lab/project_checklists/ -iname "*.txt" | \
    while read i
    do
        
        echo "### $(echo $(basename $(echo $i) | perl -pe 's/\.txt//') | perl -ne 'print uc($_)') ###"
        grep -E "^ +\.\." $i
    done | \
        grep -E -B 1 "^ +\.\." | \
        grep -v "^--" | \
        perl -pe 's/^#/\n#/'

