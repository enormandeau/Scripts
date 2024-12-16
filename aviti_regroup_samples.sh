#!/bin/bash
# Regroup all sample sequences from one AVITI run in one folder

mkdir 01_all_samples
find . | grep \.fastq\.gz$ | parallel -j 4 cp -l {} 01_all_samples
