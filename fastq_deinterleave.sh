#!/bin/bash
# Deinterleave fastq files assuming each pair of sequences has 8 lines
# Assumes the input is compressed with gzip and produces two gzip-compressed files

# Usage:
#  <program> input_fastq output_forward output_reverse

gunzip -c $1 |
    paste - - - - - - - - |
    tee >(cut -f 1-4 | tr "\t" "\n" | pigz -p 4 - > $2) |
    cut -f 5-8 | tr "\t" "\n" | pigz -p 4 - > $3
