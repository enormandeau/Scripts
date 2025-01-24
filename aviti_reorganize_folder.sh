#!/bin/bash
# Reorganize folder structure of AVITI runs to make samples more accessible and
# put run information in a folder

# Create info directory
mkdir 01_run_info

# Move all info files there
mv *.csv *.html *.json 01_run_info
mv $(find . | grep \.json$) 01_run_info

# Move all sequence files main directory
mv $(find . | grep \.fastq.gz$) .

# Delete empty directories
for i in *_R1.fastq.gz
do
    rmdir "${i%_R1.fastq.gz}"
done
