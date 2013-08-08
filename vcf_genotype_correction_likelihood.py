#!/usr/bin/python
"""Correct bad genotype calls in vcf files.

Bad genotypes are called when only a few reads support the rare variant. In
some cases, although the likelihood supports the rare variants, the individual
is being genotyped as homozygous (code 0/1). Eg:

0/1:21,3,0:1:7

will be replaced by:

1/1:21,3,0:1:7

Usage:
    ./vcf_genotype_correction.py  input_file  output_file
"""

# Importing modules
import sys

# Main
if __name__ == '__main__':
    # Parsing user input
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except:
        print __doc__
        sys.exit(1)
    
    with open(input_file) as in_f:
        with open(output_file, "w") as out_f:
            for line in in_f:
                l = line.strip()
                
                if l.startswith("#"):
                    out_f.write(l + "\n")
                    continue
                
                elif l:
                    info = l.split("\t")
                    
                    for i in xrange(9, len(info)):
                        data = info[i].split(":")
                        lh = data[1].split(",")
                        if data[0] != "./.":
                            if lh[0] == "0":
                                data[0] = "0/0"
                            elif lh[1] == "0":
                                data[0] = "0/1"
                            elif lh[2] == "0":
                                data[0] = "1/1"
                        info[i] = ":".join(data)
                    out_f.write("\t".join(info) + "\n")

