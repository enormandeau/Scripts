#!/usr/bin/env python

"""Extract wanted contigs from an .ace file into a smaller .ace file.

Wanted file contains one contig name per line.

Usage:
    %program <input_file> <wanted_file> <output_file>"""

import sys

try:
    input_file = sys.argv[1]
    wanted_file = sys.argv[2]
    output_file = sys.argv[3]
except:
    print __doc__
    sys.exit(0)

wanted = set()
with open(wanted_file) as f:
    for line in f:
        if line.strip() != "":
            wanted.add(line.strip())

wantedp = False

with open(input_file) as in_f:
    with open(output_file, "w") as out_f:
        for line in in_f:
            l = line.strip()
            if l[0:2] == "AS":
                out_f.write(line + "\n")
            if l[0:2] == "CO":
                wantedp = False
                if l.split()[1] in wanted:
                    wanted.remove(l.split()[1])
                    wantedp = True
            if wantedp == True:
                out_f.write(line)

