#!/bin/bash

echo "       -=( PROCESSING )=-"
grep -R "^ +\.\." ~/Dropbox/Lab/project_checklists/*.txt | \
    perl -pe 's/.*\///; s/\*/\t/'

