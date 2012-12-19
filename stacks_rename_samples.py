#!/usr/bin/python
"""Rename sample files automaticaly in the current directory

Usage:
    python rename_samples.py changes_file ["dryrun"]

'dryrun' is optional. If there is a second parameter, whatever it is, the
script will not modify file names but instead report on the screen what changes
it would have done.

'changes_file' is a file with 2 tab separated columns. The first column contains
an identifier that is unique to one sample and that must be changed to the value
found in the second column.

NOTE: It is CRUCIAL that the identifiers in the first column be UNIQUE
(ie: they cannot be contained within other identifiers or in the name of files
that you do not want to change).

Example 'changes_file' content:

_AACT.  DRM603
_ACAAA. DRM701
_ACCGT. LSL4001
_ACTA.  DRM601
_AGCCG. DRM703
_AGCG.  DRM686
_AGGAT. LSL4004
_ATTGA. LSL4005
_CAGA.  DRM602
_CATCT. LSL4006
"""

# Importing modules
import os
import sys

# Parsing user input
try:
    changes = sys.argv[1]
except:
    print __doc__
    sys.exit(1)

try:
    dryrun = sys.argv[2]
    if dryrun != "":
        dryrun = True
        print "--- Performing dry run ---"
    else:
        dryrun = False
except:
    dryrun = False

# Get file names from current directory
filenames = os.listdir(".")

# Reading file with changes
with open(changes) as changes_file:
    for line in changes_file:
        l = line.strip().split("\t")
        change_from, change_to = l
        change_to = "_" + change_to + "."
        for f in filenames:
            if change_from in f:
                new_name = f.replace(change_from, change_to)
                new_name = new_name.replace("sample_", "")
                if dryrun:
                    print f, "changed to -->", new_name
                else:
                    os.rename(f, new_name)
