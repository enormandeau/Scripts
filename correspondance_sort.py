#!/usr/bin/python
# -*- coding: utf-8 -*-

# Put 2 files (each with 2 columns: ID and value) in the same order
# Using a third file giving the correspondances (2 columns)

__authors__ = "Eric Normandeau"
__program_name__ = "correspondance_sort"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-03-02"


# Importing modules

import os
import sys
import getopt
import platform


# Function definitions

def help():
    """Help attained by typing './program_name.py -h'
    """
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)            User Commands         %s(1)

\033[1mNAME\033[0m
\t%s - Sort the content of 2 files

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tSort 2 files according to a third containing correspondances

\t%s Takes 3 files in. 2 contain IDs and values and a third
\tcontains correspondance for the IDs of the 2 first files. It builds
\ta new table with all the data and outputs it in a new file

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-d, --data1\033[0m
\t\tFirst data file
\t\t2 columns, tab separated (ID, value)

\t\033[1m-D, --data2\033[0m
\t\tSecond data file
\t\t2 columns, tab separated (ID, value)

\t\033[1m-c, --correspondance\033[0m
\t\tCorrespondance file
\t\t2 columns, tab separated (ID1, ID2)

\t\033[1m-o, --output\033[0m
\t\tOutput file


\033[1mAUTHORS\033[0m
\t%s

%s %s           %s          %s(1)
"""%(name, name, name, name, name, __authors__, name, __version__, \
    __revision_date__, name)
    
    if _plateform != 'Windows' and "this is great news":
        print text
    else:
        __Windows__ = "This is an abomination"
        remove = ["\033[1m","\033[0m","\033[4m"]
        for i in remove:
            text = text.replace(i, "")
        print text
        del(__Windows__) # If only we could...



# Describe the program's goal in a haiku
# --------------------------------------
# Correspondance_sort 
# Does its very best to help
# At a borring task


# The program itself
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:D:c:o:", ["help",
            "data1=", "data2=", "correspondance=", "output="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-d', '--data1'):
            input_data1 = value
        elif option in ('-D', '--data2'):
            input_data2 = value
        elif option in ('-c', '--correspondance'):
            input_corr = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(input_data1) as test:
            pass
        with open(input_data2) as test:
            pass
        with open(input_corr) as test:
            pass
    except:
        print "Input Error: One of the input files could not be found"
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print "Output Error: No output file specified or incorect path."
        print "Use -h for help."
        sys.exit(0)

    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "Authors:", __authors__
    print __copyright__
    print "Licence:", __license__


    print "Hello, program tester!"
    
    data = {}
    with open(input_data1) as f:
        for line in f:
            l = line.strip()
            if l != "":
                l = l.split("\t")
                data[l[0]] = l[1]

    with open(input_data2) as f:
        for line in f:
            l = line.strip()
            if l != "":
                l = l.split("\t")
                data[l[0]] = l[1]

    with open(input_corr) as f:
        with open(output_file, "w") as out_f:
            for line in f:
                l = line.strip()
                if l != "":
                    l = l.split("\t")
                    try:
                        out_f.write("\t".join([l[0], data[l[0]], l[1], data[l[1]]]) + "\n")
                    except:
                        print "Found a missing corresponcance combination"

