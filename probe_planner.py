#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Prepare sequences for probe design
# Prepare cDNA for Genbank submission

# Program information
__authors__ = "Eric Normandeau"
__program_name__ = "probe_planner"
__version_info__ = ('1', '2', '0')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2011-02-17"

# Todo list:
# - Add a 'computer assisted' automated gene name annotation (using the
#   protein name). See the following Biostar question:
#   http://biostar.stackexchange.com/questions/5460

# Known bugs:
# - In the case where the longuest ORF without a stop codon is not the first
#   one, the fasta sequence begins with a stop codon.


# Importing modules
import os
import sys
import getopt
import platform
import re
from Bio import SeqIO


# Class definitions
class AutoDict(dict):
    """Implementation of perl's autovivification feature
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class sequence:
    """Sequence information to choose best sequences for probe design
    """
    def __init__(self):
        self.name = ""
        self.priority = ""
        self.blast_id = ""
        self.blast_name = ""
        self.length = ""
        self.sequence = ""
        self.good_length = ""
        self.good_sequence = ""
        self.orf_length = "-99"
        self.orf_sequence = "NO_SEQUENCE"
        self.orf_aa_sequence = "NO_SEQUENCE"
        self.stop_codons = "-99"
        self.orf_begin = "-99"
        self.orf_end = "-99"
        self.strand = ""
        self.begin = ""
        self.end = ""
        self.e_value = ""
        self.complete = False
    def __str__(self):
        return str("%s  %s  %s  %s  %s  %s  %s  %s" % \
        (self.name, self.priority, self.blast_id, self.blast_name[0:31],
         self.strand, self.begin, self.end, self.e_value))
    def my_str(self):
        return str("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\
        \t%s\t%s\t%s\t%s\t%s\t%s\n" % \
        (self.name, self.priority, self.blast_id, self.blast_name,
         self.length, self.good_length, self.orf_length, self.sequence,
         self.good_sequence, self.strand, self.begin, self.end,
         self.orf_sequence, self.orf_aa_sequence, self.stop_codons,
         self.orf_begin, self.orf_end, self.e_value))

class blastplus():
    """Information about one blast result for one sequence
    """
    def __init__(self, result, sequences):
        self.result = result
        self.sequences = sequences
        self.name = find_seq_name(self.result[0])
        self.blast_id = ""
        self.good = False
        self.length = ""
        self.good_length = ""
        self.sequence = ""
        self.good_sequence = ""
        self.strand = "."
        self.begin = "."
        self.end = "."
    def is_good(self, blast_id):
        """Parse blastplus result and fill empty properties
        (strand, begin, end)
        """
        max_blast_results = 10 # Max num of blast results per search in raw blast file
        self.result_names = []
        for l in self.result[0: max_blast_results + 5]:
            if l.startswith(">"):
                break
            else:
                self.result_names.append(l)
        num_good_lines = len([l for l in self.result_names if 
                             l[0: 31].find(blast_id) > -1]) > 0
        self.good = num_good_lines > 0
        if self.good:
            self.blast_id = self.sequences[self.name].blast_id
            self.good_result = []
            write_line = False
            already_one_hit = False
            break_next_turn = False
            found_length = False
            for l in self.result:
                if break_next_turn:
                    break
                elif l.startswith(">") and self.blast_id in l[0:31]:
                    write_line = True
                elif l.startswith(">") and write_line:
                    break
                elif l.startswith(" Score =") and already_one_hit:
                    break_next_turn = True
                elif l.startswith(" Score =") and write_line:
                    already_one_hit = True
                if write_line:
                    self.good_result.append(l)
                if l.startswith("Length=") and not found_length:
                    self.length = l.split("=")[1]
                    found_length = True
            begin_end = []
            strand = 0
            for line in self.good_result:
                if line.startswith("Query "):
                    begin_end += extract_numbers(line)
                if line.startswith(" Frame = "):
                    self.strand = get_strand(line)
                elif line.startswith(" Strand="): # for blastn results
                    self.strand = 1
            try:
                begin_end = [int(x) for x in begin_end]
            except:
                print "Could not convert string to integer, returning -99"
                begin_end = [-99]
            try:
                self.begin, self.end = min(begin_end), max(begin_end)
            except:
                self.begin, self.end = -99, -99
                for line in self.good_result:
                    print line
    def __str__(self):
        return str("%s  %s  %s  %s  %s" % \
        (self.name, self.blast_id, self.strand, self.begin, self.end))


# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)      User Commands      %s(1)

\033[1mNAME\033[0m
\t%s - Prepare sequences for microarray probe design

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tClean sequences for microarray probe design

\t%s takes sequence names, fetches protein IDs and
\tnames from a file containing the best blast result for the sequences.
\tIt then recuperates strand information, evalue, and the begining
\tand the end nucleotides of the portion of the sequence that blasted
\ton the protein from a raw blastplus output file (format 6). It puts
\tall the sequences in the appropriate sense for primer design. Finally,
\tit calculates a criterion to help chose the best sequence among many
\tsequences representing the same gene in order to design the primers.

\tIf many best_blast files should be used, concatenate them in one big
\tfile. Proceed similarly for raw_blast files

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-s, --sequences\033[0m
\t\tText file, tab separated, containing sequence name
\t\tand importance index (numerical value), in two columns.

\t\033[1m-b, --best_blasts\033[0m
\t\tBest blast file, tab separated, in three columns containing
\t\tthe sequence name, the protein ID, and the protein name.

\t\033[1m-r, --raw_blasts\033[0m
\t\tRaw blast results, as outputed by blastall (format 6).

\t\033[1m-f, --fasta\033[0m
\t\tFasta file with the sequences of the analyzed genes.

\t\033[1m-o, --output\033[0m
\t\tName of project to be used for the output files.

\033[1mAUTHORS\033[0m
\t%s

%s %s       %s      %s(1)
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
        del(__Windows__) # Maybe one day...

def input_sequences(seq_file):
    """Input sequence names and importance index
    """
    sequences = {}
    with open(seq_file) as f:
        for line in f:
            line_list = line.strip().split("\t")
            if len(line_list) > 1:
                seq = sequence()
                seq.name = line_list[0]
                seq.priority = line_list[1]
                if seq.name not in sequences:
                    sequences[seq.name] = seq
    return sequences

def get_best_blast(sequences, best_blasts_file):
    """Create a dictionary of the best blasts for each sequences
    """
    count = 0
    with open(best_blasts_file) as f:
        for line in f:
            if line.strip() != "":
                blast = sequence()
                line_list = line.strip().split("\t")
                blast.name = find_seq_name(line_list[0])
                try:
                    blast.blast_id = line_list[1]
                except:
                    print line, line_list
                blast.blast_name = line_list[2]
                blast.e_value = line_list[3]
                if blast.name in sequences:
                    count += 1
                    sequences[blast.name].blast_id = blast.blast_id
                    sequences[blast.name].blast_name = blast.blast_name
                    sequences[blast.name].e_value = blast.e_value
    if count == 0:
        print "Verify that sequence names have the EXACT same format everywhere"
    return(sequences)

def blastplus_generator(raw_blasts_file):
    """Yield one blastplus result at a time
    """
    with open(raw_blasts_file) as f:
        begin = False
        while begin == False:
            l = f.readline().rstrip()
            if l.find("Query=") > -1:
                query = [l]
                begin = True
        for line in f:
            l = line.rstrip()
            if l.find("Query=") > -1:
                yield query
                query = []
            query.append(l)
        yield query

def get_raw_blast(sequences, raw_blasts_file):
    """Add strand, begin and end of blast region
    """
    blast_results = blastplus_generator(raw_blasts_file)
    blast_count = 0
    total_count = 0
    total_good = 0
    for res in blast_results:
        total_count +=1
        blast = blastplus(res, sequences)
        if blast.name in sequences:
            blast_count += 1
            blast_id = sequences[blast.name].blast_id
            blast.is_good(blast_id)
            if blast.good == True and sequences[blast.name].complete == False:
                sequences[blast.name].complete = True
                sequences[blast.name].strand = blast.strand
                sequences[blast.name].begin = blast.begin
                sequences[blast.name].end = blast.end
                sequences[blast.name].length = blast.length
                sequences[blast.name].good_length = blast.end - blast.begin + 1
                total_good += 1
    for res in blast_results: # For sequences with no good blast hit
        if blast.name in sequences:
            blast_id = sequences[blast.name].blast_id
            blast.is_good(blast_id)
            if blast.good == False and sequences[blast.name].complete == False:
                blast.good = True
                sequences[blast.name].complete = True
    return sequences

def get_fasta(sequences, fasta_file):
    """Add sequence information, trim and reverse complement as needed
    """
    fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
    end = False
    while end != True: ### Use a for loop instead!!!
        try:
            name, sequence = "SEQUENCE_NAME", "SEQUENCE_NUCLEOTIDES"
            temp_fasta = fasta_sequences.next()
            name, sequence = temp_fasta.id, temp_fasta.seq.tostring()
        except:
            end = True
        if name in sequences:
            seq = sequences[name]
            try:
                begin, end = int(seq.begin), int(seq.end)
            except:
                print seq.__dict__, "\n\n"
                seq.begin, seq.end = 1, len(sequence)
                seq.length = seq.end - seq.begin
                seq.good_length = seq.length
                seq.strand = 1
                #begin, end = int(seq.begin), int(seq.end)
            seq.sequence = sequence
            #print type(sequence)
            #print sequence
            #print seq.name
            seq.good_sequence = sequence[begin-1:end]
            try:
                strand = int(seq.strand)
            except:
                strand = 1
            if seq.complete and strand < 0:
                seq.good_sequence = reverse_complement(seq.good_sequence)
    return sequences

def output_result_table(sequences, out_file):
    """Output complete results to tab separated file
    """
    results = [x for x in sorted(sequences)]
    header = sequence()
    header.name = "Name"
    header.priority = "Priority"
    header.blast_id = "Blast_id"
    header.blast_name = "Blast_name"
    header.length = "Length"
    header.good_length = "Good_length"
    header.sequence = "Sequence"
    header.good_sequence = "Good_sequence"
    header.orf_length = "ORF_length"
    header.orf_sequence = "ORF_sequence"
    header.orf_aa_sequence = "ORF_protein"
    header.stop_codons = "Stop_codons"
    header.orf_begin = "ORF_start"
    header.orf_end = "ORF_end"
    header.strand = "Good_strand"
    header.begin = "Good_start"
    header.end = "Good_end"
    header.e_value = "E_value"
    with open(out_file + "_result_table.txt", "w") as f:
        f.write(header.my_str())
        result_count = 0
        for res in results:
            if result_count %7 == 0:
                f.write("\n")
            result_count += 1
            f.write(sequences[res].my_str())

def find_seq_name(text):
    """Use regex to find the name of the sequence being treated
    """
    return text.replace("Query=  ", "").strip()


# General utility functions

def extract_numbers(text):
    """Use regex to find numbers in a line of text
    """
    number_re = re.compile("[0-9]+")
    numbers = re.findall(number_re, text)
    return numbers

def get_strand(text):
    """Use regex to find strand information in a line of blastplus result
    """
    strand_re = re.compile(" Frame = (.[0-9])")
    try:
        strand = re.findall(strand_re, text)[0]
    except:
        strand = -99
    return strand

def complement(seq):
    """Return the complement of a DNA sequence, *NOT* it's reverse complement
    """
    if not seq.isalpha():
        print "The sequence contained non-alphabetic characters"
        print seq
    if not seq.isupper():
        print "The sequence contained non capital-letter characters"
        seq = seq.upper()
    return seq.replace("A","t").replace("T","a").replace("C",
                       "g").replace("G","c").upper()

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence
    """
    return complement(seq)[::-1]


# Translate good_sequences

def find_stop_codons(sequences):
    """Find stop codons in the sequences of a fasta file
    """
    for seq in sequences:
        sequences[seq].orf_aa_sequence = \
            translate_sequence(sequences[seq].good_sequence)
        sequences[seq].stop_codons = \
            get_stop_positions(sequences[seq])
    return sequences

def translate_sequence(seq):
    """Translate a nucleotide sequence into an amino acid chain
    
    Return it's name and sequence in a list
    """
    codon_length = 3
    chain = ""
    if len(seq) % 3 != 0: # Use assert instead
        #print "All sequence lengths must be factors of 3"
        return chain
    for codon_start in xrange(0, len(seq), 3):
        codon_end = codon_start + 3
        codon = seq[codon_start:codon_end]
        chain += translate(codon)
    return chain

def translate(codon): # VERIFY translation matrix!!!
    """Translate codons in amino acids using the XXXX code
    """
    code = {     'ttt': 'F', 'tct': 'S', 'tat': 'Y', 'tgt': 'C',
                 'ttc': 'F', 'tcc': 'S', 'tac': 'Y', 'tgc': 'C',
                 'tta': 'L', 'tca': 'S', 'taa': '*', 'tga': '*',
                 'ttg': 'L', 'tcg': 'S', 'tag': '*', 'tgg': 'W',
                 'ctt': 'L', 'cct': 'P', 'cat': 'H', 'cgt': 'R',
                 'ctc': 'L', 'ccc': 'P', 'cac': 'H', 'cgc': 'R',
                 'cta': 'L', 'cca': 'P', 'caa': 'Q', 'cga': 'R',
                 'ctg': 'L', 'ccg': 'P', 'cag': 'Q', 'cgg': 'R',
                 'att': 'I', 'act': 'T', 'aat': 'N', 'agt': 'S',
                 'atc': 'I', 'acc': 'T', 'aac': 'N', 'agc': 'S',
                 'ata': 'I', 'aca': 'T', 'aaa': 'K', 'aga': 'R',
                 'atg': 'M', 'acg': 'T', 'aag': 'K', 'agg': 'R',
                 'gtt': 'V', 'gct': 'A', 'gat': 'D', 'ggt': 'G',
                 'gtc': 'V', 'gcc': 'A', 'gac': 'D', 'ggc': 'G',
                 'gta': 'V', 'gca': 'A', 'gaa': 'E', 'gga': 'G',
                 'gtg': 'V', 'gcg': 'A', 'gag': 'E', 'ggg': 'G'
            }
    assert len(codon) == 3, "Codon of wrong length"
    assert codon.isalpha(), "Codon contains non alphabetic characters"
    codon = codon.lower().replace("u", "t")
    standard_nuc = ["a", "c", "t", "g"]
    if "n" in codon:
        return "*"
    for n in codon:
        if n not in standard_nuc:
            print "Unknown nucleotide found in codon"
    try:
        aa = code[codon]
    except:
        aa = "!"
        print "Warning! Found an inexistant codon, translating as '!'"
    return aa


# Find stop positions

def get_stop_positions(seq):
    """Get stop codon position from a list of proteins
    """
    stops = "_".join(["0"] + [str(x * 3) for x in multi_find("*", seq.orf_aa_sequence)] +
                     [str(len(seq.good_sequence))])
    return stops

def multi_find(search,text,start=0):
    positions = []
    while start > -1:
        pos = text.find(search, start)
        if pos > -1:
            positions.append(pos)
            start = pos + 1
        else:
            return positions


# Trim sequences to longuest uninterrupted ORF

def trim_orf(sequences):
    """Trim sequences to the longuest stretch of uninterrupted amino acids
    """
    for seq in sequences:
        start, stop = longuest_stretch(sequences[seq].stop_codons)
        sequences[seq].orf_begin, sequences[seq].orf_end = start, stop
        sequences[seq].orf_sequence = sequences[seq].good_sequence[start: stop]
        sequences[seq].orf_length = stop - start
    return sequences

def longuest_stretch(positions):
    """Find the longuest stretch of amino acids in a sequence
    
    Known limitation: Will keep one longuest stretch randomly in case of ties
    """
    stretches = {}
    positions = positions.split("_")
    for i in xrange(len(positions) - 1):
        start = int(positions[i])
        stop = int(positions[i + 1])
        l = stop - start
        stretches[l] = [start, stop]
    longuest = list(sorted(stretches.keys()))[-1]
    return stretches[longuest]


# Write files for Genbank submission

def write_3_fasta_files(sequences, output_file):
    """Write 3 fasta files: original, good, and ORF trimmed sequences
    """
    with open(output_file + "_original.fasta", "w") as orig_f:
        with open(output_file + "_good.fasta", "w") as good_f:
            with open(output_file + "_orf.fasta", "w") as orf_f:
                for seq in sorted(sequences):
                    n = sequences[seq].name
                    orig_s = sequences[seq].sequence
                    good_s = sequences[seq].good_sequence
                    orf_s = sequences[seq].orf_sequence
                    orig_f.write(">" + n + "\n" + orig_s + "\n")
                    good_f.write(">" + n + "\n" + good_s + "\n")
                    orf_f.write(">" + n + "\n" + orf_s + "\n")

def write_5_column_table(sequences, output_file):
    """Write 5-column table required for Genbank submission
    """
    with open(output_file + "_genbank_table.txt", "w") as f:
        for seq in sorted(sequences):
            # Cleaning the blast names. MAY REQUIRE REFINING!
            temp = sequences[seq].blast_name
            temp = re.split("; AltName: ", temp)[0]
            temp = re.split("; Short=", temp)[0]
            temp = re.split("; Flags:", temp)[0]
            temp = re.split("; Contains:", temp)[0]
            temp = re.split(" sp\|.*\|", temp)[0]
            temp = re.split(" \[[a-zA-Z(). ]*\]", temp)[0]
            blast_name = temp
            f.write(">" + sequences[seq].name + "\n")
            f.write("\t".join([str(1), 
                              str(len(sequences[seq].orf_sequence)),
                              "gene"]) + "\n")
            f.write("\t".join(["", "", "", "gene",
                              blast_name]) + "\n")
            f.write("\t".join([str(1), 
                              str(len(sequences[seq].orf_sequence)),
                              "CDS"]) + "\n")
            f.write("\t".join(["", "", "", "product",
                              blast_name]) + "\n")
            f.write("\t".join(["", "", "", "codon_start", str(1)]) + "\n")

# Probe planner, scriptish
# Wants to grow up and mature
# A full fledged program
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:b:r:o:f:", ["help",
            "sequence=", "best_blasts=", "raw_blasts=", "output=", "fasta="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-s', '--sequences'):
            sequence_file = value
        elif option in ('-b', '--best_blasts'):
            best_blasts_file = value
        elif option in ('-r', '--raw_blasts'):
            raw_blasts_file = value
        elif option in ('-f', '--fasta'):
            fasta_file = value
        elif option in ('-o', '--output'):
            output_file = value
    try:
        with open(sequence_file) as f:
            pass
    except:
        print "Input Error: No sequence file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(best_blasts_file) as f:
            pass
    except:
        print "Input Error: No best_blasts file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(raw_blasts_file) as f:
            pass
    except:
        print "Input Error: No raw_blasts file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(fasta_file) as f:
            pass
    except:
        print "Input Error: No fasta file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file + "_result_table.txt", "w") as f:
            pass
    except:
        print "Output Error: No output file specified or incorect path."
        print "Use -h for help."
        sys.exit(0)

    print
    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "By:", __authors__
    print
    
    sequences = input_sequences(sequence_file)
    sequences = get_best_blast(sequences, best_blasts_file)
    sequences = get_raw_blast(sequences, raw_blasts_file)
    sequences = get_fasta(sequences, fasta_file)
    sequences = find_stop_codons(sequences)
    sequences = trim_orf(sequences)
    write_3_fasta_files(sequences, output_file)
    write_5_column_table(sequences, output_file)
    output_result_table(sequences, output_file)

if __name__ == "__main__":
    main()

