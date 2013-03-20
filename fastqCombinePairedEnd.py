#!/usr/bin/env python
"""Recombine 2 fastq files (R1 and R2) after they have been trimmed and cleaned

Usage:
    python fastqcombinepairedend-2.py  seqheader  paireddelim  input1  input2

seqheader = Portion of sequence name common to all sequences (eg: @HWI)
paireddelim = String that separates the sequence name from the R1/R2 identifier (use " ") 
input1 = LEFT  fastq file (R1)
input2 = RIGHT fastq file (R2)
"""

# Importing modules
import sys

# Parsing user input
try:
    seqheader = sys.argv[1]
    paireddelim = sys.argv[2]
    in1 = sys.argv[3]
    in2 = sys.argv[4]
except:
    print __doc__
    sys.exit(1)

# Defining classes
class Fastq(object):
    """Fasta object with name and sequence
    """
    def __init__(self, name, seq, name2, qual):
        self.name = name
        self.shortname = self.name.split()[0]
        self.seq = seq
        self.name2 = name2
        self.qual = qual
    def getShortname(self):
        return self.shortname
    def write_to_file(self, handle):
        handle.write(self.name + "\n")
        handle.write(self.seq + "\n")
        handle.write(self.name2 + "\n")
        handle.write(self.qual + "\n")

# Defining functions
def fastq_parser(infile, seqheader):
    """Takes a fastq file infile and returns a fastq object iterator
    """
    with open(infile) as f:
        while True:
            name = f.readline().strip()
            if not name:
                break
            seq = f.readline().strip()
            name2 = f.readline().strip()
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Main
if __name__ == "__main__":
    seq1_dict = {}
    seq2_dict = {}
    seq1 = fastq_parser(in1, seqheader)
    seq2 = fastq_parser(in2, seqheader)
    with open(in1 + "_pairs_R1.fastq", "w") as out1:
        with open(in2 + "_pairs_R2.fastq", "w") as out2:
            with open(in1 + "_singles.fastq", "w") as out3:
                for s1 in seq1:
                    try:
                        s2 = seq2.next()
                    except:
                        break
                    if s1.getShortname() in seq2_dict:
                        s1.write_to_file(out1)
                        seq2_dict[s1.getShortname()].write_to_file(out2)
                        seq2_dict.pop(s1.getShortname())
                    else:
                        seq1_dict[s1.getShortname()] = s1
                    if s2.getShortname() in seq1_dict:
                        s2.write_to_file(out2)
                        seq1_dict[s2.getShortname()].write_to_file(out1)
                        seq1_dict.pop(s2.getShortname())
                    else:
                        seq2_dict[s2.getShortname()] = s2
                        
                # Treat all un paired reads
                for r in seq1_dict.values():
                    r.write_to_file(out3)
                for r in seq2_dict.values():
                    r.write_to_file(out3)

