#!/usr/bin/env python3
"""Improve compressability by modifying names and re-encode quality strings

WARNING: DO NOT USE IN PRODUCTION
    Sequence names and qualities are modified in the process. This may be fine
    for some applications but potentially catastrophic for others.

Usage:
    <program> input_fastq scheme output_fastq

"""

# Modules
import gzip
import sys

# Classes
class Fastq(object):
    """Fastq object with name, sequence, name2, and quality string
    """

    def __init__(self, name, sequence, name2, quality):
        self.name = name
        self.sequence = sequence
        self.name2 = name2
        self.quality = quality

    def write_to_file(self, handle):
        handle.write(self.name + "\n")
        handle.write(self.sequence + "\n")
        handle.write(self.name2 + "\n")
        handle.write(self.quality + "\n")

# Defining functions
def myopen(_file, mode="rt"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def quality_slim(qual):
    global quality_reduc
    """Recode quality string into 8 levels
    """

    new_qual = "".join([quality_reduc[q] for q in qual])
    return(new_qual)

def name_slim(name):
    return "@" + "s"
    #return "@" + ":".join(name.split("_")[2:])

def fastq_compressor(infile):
    """Takes a fastq file infile and returns a fastq object iterator

    Requires fastq file with four lines per sequence and no blank lines.
    """
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()
            if not name:
                break

            sequence = f.readline().strip()
            name2 = f.readline().strip()
            quality = f.readline().strip()

            yield Fastq(name_slim(name), sequence, "+", quality_slim(quality))

# Create quality reduction dictionaries for Illumina v1.8
# TODO think about where to put the new quality values:
# - Minimise SDE?
# - All values are at or above?
# - All values are at or below?
qualities =  """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJ"""
reduced = {
        "8": """$$$$''''++++000033333999999AAAAAAAGGGGGGGG""",
        "6": """&&&&&******0000006666666AAAAAAAAAGGGGGGGGG""",
        "5": """&&&&&&*******33333333==========GGGGGGGGGGG""",
        "4": """&&&&&&&&0000000000:::::::::::GGGGGGGGGGGGG""",
        "1": """GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"""
        } #     012345678901234567890123456789012345678901
          #     |    ^    |    ^    |    ^    |    ^    |

# Parse user input
try:
    input_fastq = sys.argv[1]
    scheme = sys.argv[2]
    output_fastq = sys.argv[3]
except:
    print(__doc__)
    print("Available schemes:")
    print(" ".join(list(reduced.keys())))
    sys.exit()

quality_reduc = dict(zip(qualities, reduced[scheme]))

# Treat sequences
sequences = fastq_compressor(input_fastq)

with myopen(output_fastq, "wt") as outfile:
    for s in sequences:
        s.write_to_file(outfile)
