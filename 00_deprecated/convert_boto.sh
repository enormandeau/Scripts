#!/bin/bash
FOLDER=$1

IFS=$'\n'

time for file in $(find $FOLDER -iname "*.jpg" | grep -v _small)
do
    echo $file
    NEWNAME=$(echo $file | perl -pe 's/(\.jpg|\.JPG)/_small\1/')
    convert -resize 1000x1000 -unsharp 1.0x1.0+1+0.04 $file $NEWNAME
done

