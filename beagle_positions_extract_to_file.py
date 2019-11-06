#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract all lines of a file found between a 'start' and a 'stop' markers.

Usage:
    %program <input_file> <start_marker> <stop_marker> <output_file>"""

import sys

try:
    input_file = sys.argv[1]  # Input data file
    start = sys.argv[2]       # Start marker
    stop  = sys.argv[3]       # Stop marker
    output_file = sys.argv[4] # Output data file
except:
    print __doc__
    sys.exit(0)

with open(input_file) as in_f:
    with open(output_file, "w") as out_f:
        first_line = True
        to_print = False
        for line in in_f:
            l = line.strip()

            if first_line:
                out_f.write(l + "\n")
                first_line = False
                
            if to_print == True and l.find(stop) > -1:
                out_f.write(l + "\n")
                break

            if to_print == True and l != "":
                out_f.write(l + "\n")

            elif l.find(start) > -1:
                to_print = True
                out_f.write(l + "\n")

