#!/bin/bash
# Deinterleave fasta files assuming each pair of sequences has 4 lines

# Usage:
#  <program> input_fasta output1 output2

gunzip -c $1 | paste - - - - | tee >(cut -f 1-2 | tr "\t" "\n" > $2) | cut -f 3-4 | tr "\t" "\n" > $3
