#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Print all lines of a file found between a 'start' and a 'stop' markers.

Usage:
    %program <input_file> <start_marker> <stop_marker>"""

import sys

try:
    input_file = sys.argv[1]  # Input data file
    start = sys.argv[2]       # Start marker
    stop  = sys.argv[3]       # Stop marker
except:
    print __doc__
    sys.exit(0)

with open(input_file) as in_f:
    to_print = False
    for line in in_f:
        l = line.strip()
        if to_print == True and l.find(stop) > -1:
            break
        if to_print == True:
            print l
        elif l.find(start) > -1:
            to_print = True
