#!/bin/bash

clear
echo "IMPORTANT"
grep -R "*" ~/Dropbox/Lab/project_checklists/*.txt | \
    perl -pe 's/.*\///; s/\*/\t/; s/^/  /'
echo

