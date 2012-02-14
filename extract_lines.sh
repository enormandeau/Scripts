#!/bin/bash

# $1 = fichier complet info sequences
# $2 = fichier avec noms a chercher
# $3 = fichier de sortie

for x in $(cat $2 | grep -v "^$"); do
    grep $x $1 >> $3
done

