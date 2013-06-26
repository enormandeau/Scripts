#!/bin/bash
# Add date in from of filename

file=$1
tag=$(date +%Y-%m-%d_)
untagged=$(echo $1 | perl -pe 's/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}_//')
tagged=$(echo $tag$untagged)

mv $file $tagged 2> /dev/null

