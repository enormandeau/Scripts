#!/bin/bash
# Add date in from of filename

file=$1
untagged=$(echo $1 | perl -pe 's/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}_//')

mv $file $untagged 2> /dev/null

