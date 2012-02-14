#!/usr/bin/python
# -*- coding: utf-8 -*-

# Extract the genotypes of individuals from an ACE file

__authors__ = "Eric Normandeau"
__program_name__ = "snp_genotyper"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-09-15"


# Importing modules

import os
import sys
import getopt
import platform

from scipy.stats import binom_test


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

class genotype:
    """Contain allel count for a given individual at one locus
    """
    def __init__(self, data):
        self.tag = data[2]
        try:
            self.a = int(data[3])
            self.c = int(data[4])
            self.g = int(data[5])
            self.t = int(data[6])
        except:
            print "Allel counts are not integers."
            print "Please verify input file for the presence \
of a header line."
            sys.exit(0)
    def __str__(self):
        return "%s\t%s\t%s\t%s\t%s"%(self.tag, self.a, self.c, self.g, self.t)

class locus_info:
    """Contain locus name, position, and allels
    """
    def __init__(self, data):
        self.name = data[0]
        self.pos = data[1]
        self.allel_1 = data[2]
        self.allel_2 = data[3]
    def __str__(self):
        return "%s\t%s\t%s\t%s"%(self.name, self.pos, self.allel_1, self.allel_2)

class output_format:
    """Contain individual genotypes
    """
    def __init__(self):
        self.contig = "contig"
        self.position = "position"
        self.group = "group"
        self.individual = "individual"
        self.allel_1 = "allel_1"
        self.allel_2 = "allel_2"
        self.freq_1 = "freq_1"
        self.freq_2 = "freq_2"
        self.fold_change = "fold_change"
        self.p_value = "p_value"
        self.genotype = "genotype"
    def my_str(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % \
               (str(self.contig), str(self.position), str(self.group),
                str(self.individual), str(self.allel_1), str(self.allel_2),
                str(self.freq_1), str(self.freq_2),
                str(self.fold_change), str(self.p_value), str(self.genotype))
    def useless(self):
        self.fold_change = self.p_value = "-"
    def worthless(self):
        self.allel_1 = self.allel_2 = self.freq_1 = self.freq_2 = \
        self.fold_change = self.p_value = "-"

# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                 User Commands              %s(1)

\033[1mNAME\033[0m
\t%s - Extract the genotypes of individuals

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m

\t%s uses individual SNP genotype counts as outputed by
\t'snpcount.py' and a file containing allel information for different
\tSNP loci and returns a matrix of the individual genotypes for each
\tlocus.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file, obtained from 'snpcount.py'

\t\033[1m-l, --loci\033[0m
\t\tLoci file, format (tab separated):
\t\tcontig_name\tsnp_pos\tallel1\tallel2

\t\tex:
\t\tContig_001\t231\ta\tt

\t\033[1m-o, --output\033[0m
\t\tOutput file name

\t\033[1m-e, --header\033[0m
\t\tPresence of header line in input file [y/n]

\033[1mAUTHORS\033[0m
\t%s

%s %s                %s               %s(1)
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

def process_contigs(in_file, loci_info, out_file, header):
    """Core allelic_express function.
    Pretty much does everything, using secondary functions
    """
    contigs = contig_generator(in_file, header)
    bad = 0
    good = 0
    snps = []
    with open(out_file, "w") as f:
        results = output_format()
        #f.write("contig:position\tgenotypes\n")
        while 1:
            use = -99
            individuals = []
            try:
                contig = contigs.next()
            except:
                break
            contig = [x for x in contig if "noTag" not in x[2]]
            contig_nb = contig[0][0]
            snp_pos = contig[0][1]
            if contig_nb not in loci_info:
                continue
            elif snp_pos not in loci_info[contig_nb]:
                continue
            for i in contig:
                individuals.append(genotype(i))
            sums = sum_allels(individuals)
            if is_biallelic(sums) == False:
                bad += 1
                use = False
            else:
                good += 1
                use = True
                snps.append(individuals)
                counts = sorted([sums.a, sums.c, sums.g, sums.t])
                counts.reverse()
                allels = find_allels(sums)
            f.write(str(contig_nb + ":" + snp_pos))
            for i in individuals:
                res = output_format()
                res.contig = contig_nb
                res.position = snp_pos
                res.group = i.tag.split("_")[0]
                res.individual = i.tag.split("_")[1]
                res_allels = []
                res_counts = []
                for j in allels:
                    if j == "a":
                        res_allels.append("a")
                        res_counts.append(i.a)
                    elif j == "c":
                        res_allels.append("c")
                        res_counts.append(i.c)
                    elif j == "g":
                        res_allels.append("g")
                        res_counts.append(i.g)
                    elif j == "t":
                        res_allels.append("t")
                        res_counts.append(i.t)
                res.allel_1, res.allel_2 = res_allels[0], res_allels[1]
                res.freq_1, res.freq_2 = res_counts[0], res_counts[1]
                big = max([res.freq_1, res.freq_2])
                small = min([res.freq_1, res.freq_2])
                if res.freq_1 > 0 and res.freq_2 > 0 and big/small <= 20:
                    res.genotype = res.allel_1 + "-" + res.allel_2
                elif res.freq_1 > 0:
                    res.genotype = res.allel_1 + "-" + res.allel_1
                elif res.freq_2 > 0:
                    res.genotype = res.allel_2 + "-" + res.allel_2
                else:
                    res.genotype = "NA"
                #f.write(str("\t" + res.individual + "_" + res.genotype.upper()))
                f.write(str("\t" + res.genotype.upper()))
            f.write("\n")
        print "Number of non-biallelic:", bad
        print "Number of biallelic:", good

def loci_dict(loci_file):
    """Build a dictionary of loci info
    """
    with open(loci_file) as f:
        loci_dict = AutoDict()
        for line in f:
            l = line.strip()
            if l != "":
                data = l.split("\t")
                loci_dict[data[0]][data[1]] = data[2:]
    return loci_dict

def contig_generator(in_file, header):
    """Yield the SNP data one SNP at a time
    """
    with open(in_file) as f:
        if header == True:
            junk = f.next()
            del(junk)
        last_id = ""
        for line in f:
            line_list = line.strip().split("\t")
            _id = ":".join(line_list[0:2])
            if _id == last_id:
                contig_data.append(line_list)
                last_id = _id
            elif last_id == "":
                last_id = _id
                contig_data = [line_list]
            else:
                try:
                    yield(contig_data)
                except:
                    print "All contigs treated"
                contig_data = [line_list]
                last_id = _id
        if line.strip() != "":
            yield(contig_data)

def sum_allels(individuals):
    """Compute the sum of all allel counts
    """
    sum_all = genotype(["x", "x", "sum_allels", 0, 0, 0, 0])
    for i in individuals:
        sum_all.a += i.a
        sum_all.c += i.c
        sum_all.g += i.g
        sum_all.t += i.t
    return sum_all

def is_biallelic(sums):
    """Return 'True' if locus is biallelic, 'False' otherwise
    """
    counts = [sums.a, sums.c, sums.g, sums.t]
    counts.sort()
    counts.reverse()
    total = sum(counts)
    if float(counts[0]) / total >= 0.9:
        biallelic = False
    elif float(sum(counts[0:2])) / total <= 0.98:
        biallelic = False
    else:
        biallelic = True
    return biallelic

def is_heterozygous(counts):
    hetero = True
    high = float(max(counts))
    low = float(min(counts))
    if low == high and low == 0:
        hetero = False
    elif low/high < 0.05:
        hetero = False
    return hetero

def find_allels(sums):
    """Find allel variants for diallelic snps
    """
    nuc = "a c g t".split()
    freq = [sums.a, sums.c, sums.g, sums.t]
    temp = sorted(zip(freq, nuc))
    temp.reverse()
    if temp[1][0] == temp[2][0]:
        print "Second variant is equal in count to third variant"
    return [temp[0][1], temp[1][1]]


# SNP genotyper
# Once lost in the dark
# Now shines true

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:l:o:e:", ["help",
            "input=", "loci=", "output=", "header="])
    except getopt.GetoptError, e:
        print "Input error. Use -h for help"
        sys.exit(0)
    output_file = None
    header = True
    for option, value in opts:
        if option in ('-h', '--help'):
            help()
            sys.exit(0)
        elif option in ('-i', '--input'):
            input_file = value
        elif option in ('-l', '--loci'):
            loci_file = value
        elif option in ('-o', '--output'):
            output_file = value
        elif option in ('-e', '--header'):
            if value.lower() in ["yes", "y"]:
                header = True
            elif value.lower() in ["no", "n"]:
                header = False
            else:
                print "Input Error: Header argument incorrect."
                print "Use -h for help."
                sys.exit(0)
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(loci_file) as test:
            pass
    except:
        print "Input Error: No loci file specified or file not found."
        print "Use -h for help."
        sys.exit(0)
    try:
        with open(output_file, "w") as test:
            pass
    except:
        print "Output Error: No output file specified or incorect path."
        print "Use -h for help."
        sys.exit(0)

    print "Using version:", __version__, "of", __program_name__
    print "Last revision:", __revision_date__
    print "By:", __authors__
    print
    
    # Implement cutoffs used by 'is_biallelic' function to determine if a
    #     locus is biallelic
    # Implement cutoffs used by 'is_heterozygous' function to determine if an
    #     individual is heterozygous
    
    loci_info = loci_dict(loci_file)
    process_contigs(input_file, loci_info, output_file, header)

if __name__ == "__main__":
    main()
