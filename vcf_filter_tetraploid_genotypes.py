#!/usr/bin/python
"""Recall tetraploid genotypes based on the number of reads in a vcf file
"""

# Importing modules
import argparse
import sys

# Defining classes

# Defining functions

# Main
if __name__ == '__main__':
    # Global variables
    NUM_INFO_ROWS = 9

    # Parsing user input
    parser = argparse.ArgumentParser(description=
            "Recall tetraploid genotypes based on the number of reads in a vcf file")
    parser.add_argument('-i', '--input-file', type=str, required=True,
            help='Name of the input vcf file')
    parser.add_argument('-o', '--output-file', type=str, required=True,
            help='Name of the output vcf file')
    parser.add_argument('-H', '--hom-threshold', type=int, required=True,
            help='Minimum number of sequences to call a homozygote')
    parser.add_argument('-e', '--het-threshold', type=int, required=True,
            help='Minimum number of sequences to call a heterozygote')
    parser.add_argument('-c', '--column', type=int, required=True,
            help='Column containing the number of reads')
    args = parser.parse_args()

    # Treating input file
    with open(args.input_file) as f:
        with open(args.output_file, "w") as out_f:
            for line in f:
                line = line.strip()

                # Pass empty lines
                if line == "":
                    continue

                # Calculate number of samples
                if line.find("#CHROM") >= 0:
                    split_line = line.split("\t")
                    num_samples = len(split_line) - NUM_INFO_ROWS
                    print "Treating file: ", args.input_file
                    print "Num. samples: ", num_samples

                # Output comment lines without treating them
                if line.startswith("#") or line.startswith("\"#"):
                    out_f.write(line + "\n")

                else:
                    # Extract info from the line
                    split_line = line.split("\t")

                    begin = split_line[0:NUM_INFO_ROWS]
                    genotypes_info = split_line[NUM_INFO_ROWS: NUM_INFO_ROWS + num_samples]

                    # Correct genotypes
                    corrected_genotypes = []

                    for genotype in genotypes_info:
                        print genotype
                        if genotype == ".":
                            corrected_genotypes.append(genotype)
                        else:
                            split_genotype = genotype.split(":")
                            call = split_genotype[0]
                            depth = int(split_genotype[args.column])
                            print "   Depth:", depth

                            # Homozygotes
                            if call in ["0/0/0/0", "1/1/1/1", "2/2/2/2"]:
                                if not depth >= args.hom_threshold:
                                    corrected_genotypes.append(".")
                                else:
                                    corrected_genotypes.append(genotype)

                            # Heterozygotes
                            else:
                                if not depth >= args.het_threshold:
                                    corrected_genotypes.append(".")
                                else:
                                    corrected_genotypes.append(genotype)
                    print corrected_genotypes
                    
                    # Output corrected line
                    out_f.write("\t".join(begin + corrected_genotypes) + "\n")
                            
