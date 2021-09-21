#!/usr/bin/env python3
"""Improve compressability of fastq files by modifying name and quality strings

WARNING:
    /!\  USE AT YOUR OWN RISK  /!\ 

    Sequence name and qualitie strings are modified in the process. This may be
    fine for some applications but POTENTIALLY CATASTROPHIC for others.

Usage:
    <program> input_fastq scheme name_option output_fastq

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

def quality_slim(qual, quality_reduc):
    """Recode quality string into 8 levels
    """

    new_qual = "".join([quality_reduc[q] for q in qual])
    return(new_qual)

def name_slim(name, name_option, read_num):

    if name_option == "no_name":
        return "@" + "s"
    elif name_option == "short_name":
        return "@s" + str(read_num) + " " + name.split(" ")[-1]
    elif name_option == "full_name":
        return name

def fastq_compressor(infile, quality_reduc):
    """Takes a fastq file infile and returns a fastq object iterator

    Requires fastq file with four lines per sequence and no blank lines.
    """

    read_num = 0

    with myopen(infile) as f:
        while True:
            name = f.readline().strip()
            if not name:
                break

            sequence = f.readline().strip()
            name2 = f.readline().strip()
            quality = f.readline().strip()

            read_num += 1
            yield Fastq(name_slim(name, name_option, read_num), sequence, "+", quality_slim(quality, quality_reduc))

# Parse user input
try:
    input_fastq = sys.argv[1]
    scheme = sys.argv[2]
    name_option = sys.argv[3]
    output_fastq = sys.argv[4]
except:
    print(__doc__)
    sys.exit()

# Create quality reduction dictionaries for Illumina v1.8
# TODO think about where to put the new quality values:
# - Minimise SDE?
# - All values are at or above?
# - All values are at or below?
qualities =  """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJ"""
novasequal = """  #         -         7    <    A    F   J"""
reduced = {
        "7": """######--------7777777777<<<<<AAAAAAAFFFJJJ""",
        "5": """######--------7777777777AAAAAAAAAAAAFFFFFF""",
        "4": """######---------7777777777FFFFFFFFFFFFFFFFF""",
        "3": """######--------------FFFFFFFFFFFFFFFFFFFFFF""",
        "2": """######GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"""
        } #     012345678901234567890123456789012345678901
          #     |    ^    |    ^    |    ^    |    ^    |
          #
# Assert input
if not scheme in reduced:
    print(__doc__)
    print("Available schemes: " + " ".join(list(reduced.keys())))
    sys.exit(1)

if not name_option in ["no_name", "short_name", "full_name"]:
    print(__doc__)
    print("""Available name options: "no_name", "short_name", and "full_name" """)
    sys.exit(1)

quality_reduc = dict(zip(qualities, reduced[scheme]))

# Treat sequences
sequences = fastq_compressor(input_fastq, quality_reduc)

with myopen(output_fastq, "wt") as outfile:
    for s in sequences:
        s.write_to_file(outfile)
