#!/usr/bin/env python3
"""Extract GC proportion using a sliding window

Usage:
    <program> input_fasta window_size output_file
"""

# Modules
import sys

from collections import Counter
from scipy import stats

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Classes
class Fasta(object):
    """Fasta object with name and sequence
    """

    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

    def write_to_file(self, handle):
        handle.write(">" + self.name + "\n")
        handle.write(self.sequence + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

class Fastq(object):
    """Fastq object with name, sequence, name2, and quality string
    """

    def __init__(self, name, sequence, name2, quality):
        self.name = name
        self.sequence = sequence
        self.name2 = name2
        self.quality = quality

    def getShortname(self, separator):
        if separator:
            self.temp = self.name.split(separator)
            del(self.temp[-1])
            return separator.join(self.temp)

        else:
            return self.name

    def write_to_file(self, handle):
        handle.write(self.name + "\n")
        handle.write(self.sequence + "\n")
        handle.write(self.name2 + "\n")
        handle.write(self.quality + "\n")

    def __repr__(self):
        return self.name + " " + self.sequence[:31]

# Defining functions
def myopen(_file, mode="r"):
    if _file.endswith(".gz"):
        return gzip.open(_file, mode=mode)

    else:
        return open(_file, mode=mode)

def fasta_iterator(input_file):
    """Takes a fasta file input_file and returns a fasta iterator
    """
    with myopen(input_file) as f:
        sequence = ""
        name = ""
        begun = False

        for line in f:
            line = line.strip()

            if line.startswith(">"):
                if begun:
                    yield Fasta(name, sequence)

                name = line[1:]
                sequence = ""
                begun = True

            else:
                sequence += line

        if name != "":
            yield Fasta(name, sequence)

def fastq_iterator(infile):
    """Takes a fastq file infile and returns a fastq object iterator

    Requires fastq file with four lines per sequence and no blank lines.
    """
    
    with myopen(infile) as f:
        while True:
            name = f.readline().strip()

            if not name:
                break

            seq = f.readline().strip()
            name2 = f.readline().strip()
            qual = f.readline().strip()
            yield Fastq(name, seq, name2, qual)

# Parse user input
try:
    input_fasta = sys.argv[1]
    window_size = int(sys.argv[2])
    output_file = sys.argv[3]
except:
    print(__doc__)
    sys.exit(1)

# Read input file and compute GC content per window size
sequences = fasta_iterator(input_fasta)
gc_values = []

for s in sequences:
    remaining = s.sequence.upper()
    name = s.name
    pos = -1 * int(window_size / 2)

    while len(remaining) >= window_size:
        pos += window_size
        counter = Counter(remaining[:window_size])
        remaining = remaining[window_size:]
        try:
            gc_values.append((name, pos, float(counter["C"] + counter["G"]) / float(window_size - counter["N"])))
        except:
            pass

# Write values to file
with open(output_file, "w") as outfile:
    for gc in sorted(gc_values):
        outfile.write("\t".join([str(x) for x in gc]) + "\n")

# Produce GC histogram
gc = [x[2] for x in gc_values]
plot = sns.distplot(gc,
        bins=25,
        kde=False,
        hist_kws={'edgecolor':'darkblue'},
        fit=stats.gamma)

plt.xlabel("GC content")
plt.ylabel("Frequency")
plt.title("Distribution of GC content")
average_gc = str(round(sum(gc) / float(len(gc)), 3))
plt.text(0.8, 5.7, "GC = " + average_gc, fontsize=10)
plt.xlim(0, 1)
plt.ylim(0, 6)

fig = plot.get_figure()
fig.savefig(output_file + ".png")
