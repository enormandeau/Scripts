#!/usr/bin/python
"""Filter called genotypes in a vcf file

USAGE:
    python vcf_filter_tetraploid_genotypes.py input output homozygote heterozygote

input = name of input vcf file
output = name of output vcf file
homozygote = mininum number of sequences to call a homozygous genotype
heterozygote = mininum number of sequences to call a heterozygote genotype
"""

# Importing modules
import sys

# Defining classes

# Defining functions

# Main
if __name__ == '__main__':
    # Global variables
    ROWS_BEFORE = 9

    # Parsing user input
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        hom_threshold = int(sys.argv[3])
        het_threshold = int(sys.argv[4])
    except:
        print __doc__
        sys.exit(1)

    # Treating input file
    with open(input_file) as f:
        with open(output_file, "w") as out_f:
            for line in f:
                line = line.strip()

                # Pass empty lines
                if line == "":
                    continue

                # Calculate number of samples
                if line.find("#CHROM") >= 0:
                    split_line = line.split("\t")
                    num_samples = len(split_line) - ROWS_BEFORE
                    print "Treating", input_file
                    print "Num. samples:", num_samples

                # Output comment lines without treating them
                if line.startswith("#") or line.startswith("\"#"):
                    out_f.write(line + "\n")

                else:
                    # Extract info from the line
                    split_line = line.split("\t")

                    begin = split_line[0:ROWS_BEFORE]
                    genotypes_info = split_line[ROWS_BEFORE: ROWS_BEFORE + num_samples]

                    # Correct genotypes
                    corrected_genotypes = []

                    for genotype in genotypes_info:
                        if genotype == ".":
                            corrected_genotypes.append(genotype)
                        else:
                            split_genotype = genotype.split(":")
                            call = split_genotype[0]
                            depth = int(split_genotype[2])

                            # Homozygotes
                            if call in ["0/0/0/0", "1/1/1/1", "2/2/2/2"]:
                                if not depth >= hom_threshold:
                                    corrected_genotypes.append(".")
                                else:
                                    corrected_genotypes.append(genotype)

                            # Heterozygotes
                            else:
                                if not depth >= het_threshold:
                                    corrected_genotypes.append(".")
                                else:
                                    corrected_genotypes.append(genotype)
                    
                    # Output corrected line
                    out_f.write("\t".join(begin + corrected_genotypes) + "\n")
                            
