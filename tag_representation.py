## Eric Normandeau
## 2010-02-16


# Find tag representation in 454 data


## GLOBAL VARIABLES to be changed by user

INPUT_TAGS = r"C:\Python26\_projects\berenice\adapteurs_reduced.fa"
INPUT_FASTA = r"C:\Python26\_projects\berenice\LD_1-8.fa"  ##  DR_1-2.fa  DR_1-8.fa  LD_1-2.fa  LD_1-8.fa

## Module imports

from copy import deepcopy
import math


## Function definitions

def readfasta(path):
    """
    Read FASTA file and put it in a list of lists, each inner list containing
    a name and a sequence
    
    """
    out = []
    line_counter = -1
    file = open(path)
    for line in file:
        if line.startswith(">"):
            contig_name = line.split()[0]
            contig_seq = ""
            out.append([contig_name, contig_seq])
        else:
            out[line_counter][1] += line.rstrip()
    file.close()
    return out

def writefasta(var, path, line_return = 60):
    """
    Write FASTA file from a list of lists, each inner list containing one
    or more FASTA objects separated each in two string objects
    
    """
    file = open(path, "w")
    for line in var:
        for item in line:
            if item.startswith(">"):
                file.write(item + "\n")
            else:
                if line_return == 0:
                    file.write(item + "\n")
                else:
                    while len(item) > 0:
                        file.write(item[:line_return] + "\n")
                        item = item[line_return:]
    file.close()

###########################
## Find tag representation


tags = readfasta(INPUT_TAGS)
seqs = readfasta(INPUT_FASTA)

print "No. tags: " + str(len(tags)) + "   No. seqs: " + str(len(seqs))
tag_dict = {}

for tag in tags:
    name = tag[0]
    tag_dict[name] = 0

for seq in seqs:
    fasta_seq = seq[1]
    for tag in tags:
        tag_name = tag[0]
        tag_seq = tag[1]
        if fasta_seq.startswith(tag_seq):
            tag_dict[tag_name] += 1

tag_count = sorted(tag_dict.items())
total = 0

for i in tag_count:
    total += i[1]
    print i[0], i[1]

print "Total of taged sequences =", total
print 100 * total / len(seqs), "% of sequences are tagged"


