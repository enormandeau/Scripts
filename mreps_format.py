#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Format output of mreps to a usable format.

Usage:
    %program <mreps_output> <sequence_file> <annot_file> <formated_result>"""

import sys
from Bio import SeqIO
from collections import defaultdict
from copy import deepcopy

class sequence():
    def __init__(self, line):
        line = line.split("\t")
        self.name = line[0].strip()
        self.start = line[1].strip()
        self.end = line[2].strip()
        self.length = line[3].strip()
        self.period = line[4].strip()
        self.n_repeats = line[5].strip()
        self.error_rate = line[6].strip()
        self.repeat = line[7].strip()
        self.sequence = line[8].strip()
        self.annotation = line[9].strip()
        self.flank_right = str(len(self.sequence) - int(self.end))
    def __str__(self):
        return "\t".join([self.name, self.start, self.end, self.length,
                          self.flank_right, self.period, self.n_repeats,
                          self.error_rate, self.repeat, self.sequence,
                          self.annotation])

try:
    in_file = sys.argv[1]
    seq_file = sys.argv[2]
    annot_file = sys.argv[3]
    out_file = sys.argv[4]
except:
    print __doc__
    sys.exit(0)

with open(seq_file) as f:
    seq_dict = SeqIO.to_dict(SeqIO.parse(f, "fasta"))

with open(annot_file) as f:
    annot_dict = {}
    for line in f:
        if line.strip() != "":
            l = line.strip()
            l = l.split("\t")
            annot_dict[l[0]] = l[2]

title_line = "name\tstart\tend\tlength\tflank_right\t\
period\tn_repeats\terror_rate\trepeat\tsequence\tannotation\n"

with open(out_file, "w") as out_f:
    out_f.write(title_line)
    with open(in_file) as f:
        for line in f:
            if line.strip() != "":
                l = line.strip()
                try:
                    int(l.split()[0])
                    l = name + "\t" + l
                except:
                    name = l.split()[0]
                seq = seq_dict[name].seq.tostring()
                annot = annot_dict[name]
                l += "\t" + seq + "\t" + annot
                l = l.replace(":", "").replace("->", "").replace("  ", "\t").replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").replace("\t \t", "\t")
                l = sequence(l)
                out_f.write(str(l) + "\n")



