#!/usr/bin/python
"""Print a progress bar given a total and a current progress

USAGE:
    %program total progress

EXAMPLE:
    progress_bar.py 30 18

gives:

<==================------------>

"""
import sys

try:
    total = int(sys.argv[1])
    progress = int(sys.argv[2])
except:
    print __doc__
    sys.exit(1)

print "<" + progress * "=" + (total - progress) * "-" + ">\n"

