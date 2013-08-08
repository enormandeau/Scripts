# Preparing SNP detection for coregonus
#
# Eric Normandeau 2010-02-10

# Import modules
import re
import string
import math
from copy import copy

# Function definitions
def readfile(path):
    """Read file and return a list containing the file lines"""
    out = []
    file = open(path, "r")
    for line in file:
        out.append(line)
    file.close()
    return out

def writefile(var, path):
    """Write lines from the first dimension of structuring of an object"""
    file = open(path, "w")
    for line in var:
        file.write(line)
    file.close()

def readfasta(path):
    """Read FASTA file and put it in a list of lists, each inner list containing a name and a sequence"""
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

def writefasta(var, path, ncar=60):
    """Write FASTA file from a list of lists, each inner list containing one or more FASTA objects separated each in two string objects"""
    file = open(path, "w")
    for line in var:
        for item in line:
            if item.startswith(">"):
                file.write(item + "\n")
            else:
                while len(item) > 0:
                    file.write(item[:ncar] + "\n")
                    item = item[ncar:]
    file.close()


# Modifying the fasta names
INPUT_FASTA = r"C:\Python26\_projects\PAG\Aro_Inter3_13661_Contigs.fa"
OUTPUT_FASTA = r"C:\Python26\_projects\PAG\Aro_Inter3_13661_Contigs_renamed.fa"

fasta_data = readfasta(INPUT_FASTA)

fasta_out = [[">Contig" + str("%05i" % int(re.findall("Contig([0-9]+)", fasta[0])[0])), fasta[1]] for fasta in fasta_data]

writefasta(fasta_out, OUTPUT_FASTA)


# Parsing blast result
# After blast+
# No format
BLAST_INPUT = r"C:\Python26\_projects\PAG\Aro_Inter_13661_res.txt"
BLAST_OUTPUT = r"C:\Python26\_projects\PAG\_output_Aro_Inter_13661_res_parsed.txt"

blast = readfile(BLAST_INPUT)

blast_list = []

input_file = open(BLAST_INPUT, "r")

current_blast = "ContigName\tGeneID\tGeneName\tBitScore\teValue"

for line in input_file:
    if line.startswith("Query="):
        blast_list.append(current_blast + "\n")
        complete = 0
        current_blast = line.split()[-1].strip()
    elif line.startswith(">sp") and complete == 0:
#        current_blast += "\t" + "".join("\t".split(line[1:].strip()))
        current_blast += "\t" + line[1:].split("Full=")[0].split(" ")[0]
        current_blast += "\t" + "\t".join(line[1:].split("Full=")[-1].strip().split(";", 0)).strip()
    elif line.startswith("***** No hits found *****") and complete == 0:
        current_blast += "\t" + line.strip()
        complete = 1
    elif line.startswith(" Score = ") and complete == 0:
        current_blast += "\t" + "\t".join(line.strip().split(","))
        complete = 1
    elif line.startswith(" Identities = ") and complete == 0:
        current_blast += "\t" + line.strip()
        complete = 1

blast_list.append(current_blast + "\n")

writefile(blast_list, BLAST_OUTPUT)










