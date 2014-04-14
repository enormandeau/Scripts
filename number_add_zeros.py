#!/usr/bin/env python

"""Pad all numbers of a file with zeros to a specified number of characters.

Additionally, zero-padded numbers can be preceded by a string stub.
    eg: 123 could become: orange_000123

Usage:
    %program <input_file> <output_file> [number_characters] [stub]"""

import sys
import re

try:
    in_file = open(sys.argv[1], "rU")
    out_file = open(sys.argv[2], "w")
except:
    print __doc__
    sys.exit(0)

try:
    num_zeros = int(sys.argv[3])
except:
    print "No valid number of zeroes was entered, using 4 as default"
    num_zeros = 4

try:
    stub = str(sys.argv[4])
except:
    print "No or bad stub specified. Adding no stub."
    stub = ""

lines = [line.strip() for line in in_file.readlines() if line.strip() != ""]
zero_format = "%0" + str(num_zeros) + "i"

with open(sys.argv[2], "w") as out_file:
    for l in lines:
        try:
            num = re.findall("[0-9]+", l)
        except:
            continue
        if len(num) > -1:
            for n in num:
                l = l.replace(n, str(zero_format % int(n)))
        out_file.write(stub + l + "\n")
