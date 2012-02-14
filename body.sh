#!/bin/bash

# Extracting lines from the middle of a file. Similar to head and tail
# Extract <n> lines from <begin line> in file <filename>

# $1 = begin line
# $2 = n. of lines
# $3 = filename

end=$(( $1 + $2 ))
head -n $end $3 | tail -n $2

