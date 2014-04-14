#!/usr/bin/env python
"""Extract start end positions of sequences that blast on transposons

Usage:
    program_name <tblastx_result_file>
"""

# Importing modules
import sys
import re


# Parsing user input
try:
    infile = sys.argv[1]
except:
    print __doc__
    sys.exit(1)


# Defining functions
def blastplus(raw_blasts_file):
    """Return list of results
    """
    with open(raw_blasts_file) as f:
        results = []
        begin = False
        while begin == False:
            l = f.readline().rstrip()
            if l.find("Query=") > -1:
                query = [l]
                begin = True
        for line in f:
            l = line.rstrip()
            if l.find("Query=") > -1:
                if not '***** No hits found *****' in query:
                    results.append(query)
                else:
                    query.append("Query 0 ACTG 999999999")
                    results.append(query)
                query = []
            query.append(l)
        return results

def extract_lines(results):
    lines = []
    for r in results:
        for l in r:
            if l.startswith("Query="):
                lines.append(l)
            elif l.startswith("Query") or l.startswith(" Score") or l.startswith(">"):
                lines.append(l)
    return lines

def extract_numbers(text):
    """Use regex to find numbers in a line of text
    """
    number_re = re.compile("[0-9]+")
    numbers = [int(n) for n in re.findall(number_re, text)]
    return numbers

def bunch_good_lines(lines):
    good = []
    temp = ["First line"]
    numbers = [0, 99]
    ended = begun = False
    for l in lines:
        if l.startswith("Query="):
            begin, end = str(min(numbers)), str(max(numbers))
            temp += [begin, end]
            good.append("\t".join(temp))
            temp = [l.replace("Query= ", "")]
            numbers = []
            ended = begun = False
        elif l.startswith("Query ") and ended == False:
            begun = True
            numbers += (extract_numbers(l))
        elif l.startswith("Query=") and begun == True:
            ended = True
        elif l.startswith(" Score") and begun == True:
            ended = True
        elif l.startswith(">") and begun == True:
            ended = True
    return good


# Main
if __name__ == '__main__':
    results = blastplus(infile)
    lines = extract_lines(results)
    good = bunch_good_lines(lines)
    for g in good:
        print g





















