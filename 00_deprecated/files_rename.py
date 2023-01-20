#!/usr/bin/env python
"""
Rename files according to a file containing old and new names in the following
format:

oldfile1 (tabulation) newfile1
oldfile2 (tabulation) newfile2
...
oldfileN (tabulation) newfileN

You get the idea. Usage:

./rename.py infile

Where infile contains the old and new names
"""
import sys
from subprocess import call

try:
    infile = sys.argv[1]
except:
    print __doc__
    sys.exit(1)

names = [[x.strip().split("\t")[0], x.strip().split("\t")[1]]
         for x in open(infile).readlines() if x.strip() != ""]

for old, new in names:
    call(str("cp '%s' new_'%s'" % (old, new)),shell=True)
