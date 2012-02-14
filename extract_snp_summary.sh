#!/usr/bin/env bash

clear
echo "Extracting SNP results from RADtools output file"
echo "------------------------------------------------"
echo "Running..."
grep "^[0-9]" $1 | sed 's/M//g' >$2
echo "Done!"
echo
pwd
echo "Summary extracted to file: $2"
echo

