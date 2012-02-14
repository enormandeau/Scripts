#!/usr/bin/python
# -*- coding: utf-8 -*-

# Template to create new programs

__authors__ = "Eric Normandeau"
__program_name__ = "program_template"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-01-14"


# Importing modules

import os
import sys
import getopt
import platform


# Exception definitions

class ProgramTemplate(Exception): pass
class BadInput(ProgramTemplate): pass
class OtherTest(ProgramTemplate): pass


# Class definitions

class MyClass:
    """My class
    """
    pass


# Function definitions

def help():
    """Help attained by typing './program_name.py -h'
    """
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)            User Commands         %s(1)

\033[1mNAME\033[0m
\t%s - Short description

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tOne line description

\t%s Does this and that from this and thas files.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file

\t\033[1m-o, --output\033[0m
\t\tOutput file

\t\033[1m-O, --other\033[0m
\t\tOther file needed

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

def fun_1(x):
    """First function
    
    Thoroughly tested with 'unittest' in 'program_template_test.py'
    """
    if not isinstance(x, str):
        raise BadInput, "Input must be a string!"
    return x


# Describe the program's goal in a haiku
# --------------------------------------
# Hi, program_template
# Your future, like the moon, shines
# Filled with bright success


# The program itself
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:O:", ["help",
            "input=", "output=", "other="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-o', '--output'):
            output_file = value
        elif option in ('-O', '--other'):
            other_file = value
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print "Output Error: No output file specified or incorect path."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(other_file) as test:
            pass
    except:
        print "Input Error: No 'other' file specified or file not found."
        print "Use -h for help."
        sys.exit(0)

    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "Authors:", __authors__
    print

    fun_1("allo")
    fun_2("roger")

