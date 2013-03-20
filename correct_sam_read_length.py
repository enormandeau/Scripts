#!/usr/bin/python
"""Keep only lines from a SAM file where the sequence length matches the info in column 6 

Usage:
    ./correct_sam_read_length.py input_file
"""

# Import modules
import sys
import re

# Defining functions
def find_numbers(text):
    """Find all numbers from string and return list of numbers
    """
    number_re = re.compile("([0-9]+)[^D]")
    numbers = [int(n) for n in re.findall(number_re, text)]
    return numbers

# Main
if __name__ == '__main__':
    # Parsing user input
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except:
        print __doc__
        sys.exit(1)

    # open input file
    with open(input_file) as f:
        # open output file
        with open(output_file, "w") as outf:
            for line1 in f:
                if line1.startswith("@"):
                    outf.write(line1) 
                    continue
                else:
                    line1 = line1.strip()
                    write_to_file = True
                    line2 = f.next()
                    line2 = line2.strip()
                    columns1 = line1.split("\t")
                    info1 = columns1[5]
                    columns2 = line2.split("\t")
                    info2 = columns2[5]
                    if info1 == "*" and info2 == "*":
                        pass
                    elif info1 == "*":
                        name2 = columns2[0]
                        info2 = "".join(re.split("[0-9]+D", info2))
                        sum_info2 = sum(find_numbers(info2))
                        seq2 = columns2[9]
                        if sum_info2 != len(seq2):
                            print "line2 = problem"
                            write_to_file = False
                    elif info2 == "*":
                        name1 = columns1[0]
                        info1 = "".join(re.split("[0-9]+D", info1))
                        sum_info1 = sum(find_numbers(info1))
                        seq1 = columns1[9]
                        if sum_info1 != len(seq1):
                            print "line1 = problem --"
                            write_to_file = False
                    else:
                        # Extract info from line1
                        name1 = columns1[0]
                        info1 = "".join(re.split("[0-9]+D", info1))
                        sum_info1 = sum(find_numbers(info1))
                        seq1 = columns1[9]
                        # Same for line2
                        name2 = columns2[0]
                        info2 = "".join(re.split("[0-9]+D", info2))
                        sum_info2 = sum(find_numbers(info2))
                        seq2 = columns2[9]
                        if sum_info1 != len(seq1) or sum_info2 != len(seq2):
                            write_to_file = False
                            print name1, info1, sum_info1, len(seq1)
                            print name2, info2, sum_info2, len(seq2)
                if write_to_file:
                    # write to file
                    outf.write(line1 + "\n")
                    outf.write(line2 + "\n")

