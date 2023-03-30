#!/usr/bin/env python3
"""Split beagle (can be gzip-compressed) into multiple beagle files with split_num samples each

Usage:
    <program> input_beagle split_num
"""


# Modules
import math
import gzip
import sys

# Functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)
    else:
        return open(_file, mode=mode)

# Parsing user input
try:
    input_beagle = sys.argv[1]
    split_num = int(sys.argv[2])
except:
    print(__doc__)
    sys.exit(1)

# Let's go
output_handles = {}

with myopen(input_beagle) as infile:
    for line in infile:
        l = line.strip().split("\t")
        info = l[: 3]
        data = l[3: ]

        if line.startswith("marker"):
            num_samples = int(len(data)/3)
            num_files = math.ceil(num_samples / split_num)

            for i in range(num_files):
                output_handles[i] = myopen(("split_" + str(i) + ".beagle"), "wt")

        for i in range(num_files):
            new_line = info[:]
            new_line += data[: split_num]
            data = data[split_num: ]

            output_handles[i].write("\t".join(new_line) + "\n")
