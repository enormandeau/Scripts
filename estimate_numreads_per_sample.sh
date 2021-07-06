#!/bin/bash
# Estimate the number of reads in .fastq.gz and accurately count those in .bam files from a folder
#
# Usage:
#     <program> input_folder

# Global variables
input_folder="$1"
output_file=numreads_per_sample_"${input_folder%/}"
rm $output_file 2>/dev/null
module load samtools 2>/dev/null

# Fastq files
for fastq in $(ls -1 "$input_folder"/*.fastq.gz "$input_folder"/*.fq.gz 2>/dev/null)
do
    base=$(basename "$fastq")
    temp=."$base".deleteme

    # Extract last 10K of the first 50K reads
    gunzip -c "$fastq" | head -200000 | tail -40000 | gzip -c - > "$temp"
    size_subset=$(ls -l "$temp" | awk '{print $5}')
    size_full=$(ls -l "$fastq" | awk '{print $5}')
    numreads=$(echo 10000 $size_subset $size_full | awk '{print $1 * $3 / $2}')
    echo -e "$base\t$numreads"
    rm "$temp"
done | tee "$output_file"_fastq

# Cleanup if output file is empty
[ -s "$output_file"_fastq ] ||  rm "$output_file"_fastq

# Bam files
for bamfile in $(ls -1 "$input_folder"/*.bam 2>/dev/null)
do
    base=$(basename "$bamfile")
    numreads=$(samtools idxstats "$bamfile" | awk '{s+=$3}END{print s}')
    echo -e "$base\t$numreads"
done | tee "$output_file"_bam

# Cleanup if output file is empty
[ -s "$output_file"_bam ] || rm "$output_file"_bam
