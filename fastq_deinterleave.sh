#!/bin/bash
# Deinterleave fastq files assuming each pair of sequences has 8 lines

# Usage:
#  <program> input_fastq output1 output2

gunzip -c $1 | paste - - - - - - - - | tee >(cut -f 1-4 | tr "\t" "\n" > $2) | cut -f 5-8 | tr "\t" "\n" > $3
