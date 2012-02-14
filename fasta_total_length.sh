#!/bin/bash

# Experimental, should NOT be used
echo "This program is HIGHLY EXPERIMENTAL"
echo "It should NOT be used for serious purposes"
echo

n=`grep -v ">" "$1" | wc -c`
echo "The fasta file has a total of $n nucleotides"
