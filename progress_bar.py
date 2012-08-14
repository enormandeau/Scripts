#!/usr/bin/python
"""Print a progress bar given a total and a current progress

USAGE:
    %program total progress

EXAMPLE:
    progress_bar.py 30 18 [name of process]

gives:

process_name number_done: 3/30 (===---------------------------) 10.0%

"""
import sys

try:
    number_total = int(sys.argv[1])
    number_done = int(sys.argv[2])
except:
    print __doc__
    sys.exit(1)

percent_done = 100. * number_done / number_total
#percent_done = str("%3.1f" % (100. * number_done / number_total))

print "number_done: " + str(number_done) + "/" + str(number_total) + " (" + int(percent_done * 0.3) * "=" + int((100 - percent_done) * 0.3) * "-" + ") " + str("%3.1f" % percent_done) + "%"

