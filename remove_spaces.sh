#!/bin/bash

echo "This program is HIGHLY EXPERIMENTAL"
echo "It should NOT be used on your system"
echo "NOTE: the dangerous line is commented out"
echo

IFS='
'
j=`find $1 -printf "%d\n" | sort -u | tail -n 1`
j=$((j-1))
echo "Max dir depth:" $j
for (( i=0; i<=j ; i++ ))
    do
    for name in `find -mindepth $i -maxdepth $i -iname "* *" -printf "%p\n"`
        do
            newname=`echo "$name" | tr " " "_"`
            echo "$name" "$newname"
#            mv "$name" "$newname"
        done
done
########## 
