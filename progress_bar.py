#!/usr/bin/env python
"""Print a progress bar given a total and a current progress

USAGE:
    %program total progress

EXAMPLE:
    progress_bar.py 30 18 [name of process]

gives:

process_name number_done: 3/30 (===                           ) 10.0%

"""
import sys
import math

try:
    number_total = int(sys.argv[1])
    number_done = int(sys.argv[2])
except:
    print __doc__
    sys.exit(1)

try:
    process_name = sys.argv[3]
except:
    process_name = "progress"

try:
    percent_done = 100. * number_done / number_total
except:
    percent_done = 0

name = process_name + ": "
name = name + (16 - len(name)) * " "

numbers = str(number_done) + "/" + str(number_total) + " "
numbers = numbers + (8 - len(numbers)) * " "

progress = int(math.floor(percent_done * 0.3)) * "="
progress = progress + (30 - len(progress)) * " "
progress = "(" + progress + ") "

percent = str("%3.1f" % percent_done) + "%"

print name + numbers + progress + percent

"""
Processes:
sai:        60/60    (==================================================) 100.0%
sam:        60/60    (==================================================) 100.0%
STACKS_fq1: 10/30    (================                                  ) 33.3%
STACKS_fq1: 3/30     (=====                                             ) 10.0%
"""
