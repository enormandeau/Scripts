#!/usr/bin/python
# -*- coding: utf-8 -*-

# Explore allelic expression imbalance results

__authors__ = "Eric Normandeau"
__program_name__ = "allele_expression_summary"
__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-07-08"


# Importing modules

import os
import sys
import getopt
import platform

from collections import defaultdict

from scipy.stats import binom_test
from math import copysign


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
    """Hold individual genotype data
    """
    def __init__(self, lis):
        self.group = lis[0]
        self.ind = lis[1]
        self.allel_1 = lis[2]
        self.allel_2 = lis[3]
        self.freq_1 = lis[4]
        self.freq_2 = lis[5]
        self.fold_change = lis[6]
        self.p_value = lis[7]
    def __str__(self):
        return str("%s  %s  %s  %s" % (self.group, self.ind, 
                   self.fold_change, self.p_value))


# Function definitions

def help():
    _plateform = platform.system()
    name = __program_name__
    text =  """
%s(1)                 User Commands              %s(1)

\033[1mNAME\033[0m
\t%s - Allelic expression imbalance results exploration

\033[1mSYNOPSIS\033[0m
\t\033[1mpython %s.py \033[0m[\033[4mOPTION\033[0m]    [\033[4mFILE\033[0m]...

\033[1mDESCRIPTION\033[0m
\tSummarizes allelic expression imbalance results

\t%s uses the output file from 'allelic_express.py' to explore the
\tmeaning and characteristics of the results.

\033[1mOPTIONS\033[0m
\t\033[1m-h, --help\033[0m
\t\tDisplay the help of this program

\t\033[1m-i, --input\033[0m
\t\tInput file, obtained from 'allelic_express.py'

\t\033[1m-o, --output\033[0m
\t\tOutput text file, in tab separated format.
\t\tSee output format example below.

\t\033[1m-e, --header\033[0m
\t\tPresence of header line in input file [y/n] Default to yes

\t\033[1m-a, --alpha\033[0m
\t\tAlpha level, maximum pvalue deemed significant

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
        del(__Windows__) # Keep dreaming...

def explore_allelic_imbalance(in_file, out_file, header, alpha):
    """Core allelic_express function.
    Pretty much does everything, using secondary functions
    """
    snp_dict = defaultdict(list)
    groups = set()
    with open(in_file) as f:
        if header == True:
            junk = f.next()
            del(junk)
        for line in f:
            line_list = line.strip().split("\t")
            groups.add(line_list[2])
            contig_nb = str("%05i" % int(line_list[0].split("_")[1]))
            snp_pos = str("%04i" % int(line_list[1]))
            _id = ":".join(["Contig_" + contig_nb, snp_pos])
            snp_dict[_id].append(line_list[2:])
    good_snp_dict = filter_snps(snp_dict, groups, out_file)
    output_results(good_snp_dict, out_file, groups, alpha)

def filter_snps(snp_dict, groups, out_file, min_ind=3, max_ind=12):
    """Remove SNPs with unwanted characteristics.
       Eg: Too many heterozygous individuals (paralogues)
       No or too few heterozygous individuals (to few data)
    """
    skimmed_dict = AutoDict()
    for i in snp_dict:           # Iterate over SNPs
        temp_dict = defaultdict(list)
        temp_groups = defaultdict(int)
        for j in snp_dict[i]:    # Iterate over variants
            if j[-1] != "-":
                temp_dict[i].append(j)
                for k in groups: # Iterate over groups
                    if j[0] == k:
                        temp_groups[k] += 1
        for k in temp_groups:
            if temp_groups[k] < min_ind:
                temp_groups[k] = 0
        group_counts = temp_groups.values()
        num_hetero = len(temp_dict[i]) 
        if num_hetero <= max_ind and len(group_counts) > 0:
# old            if min(group_counts) >= min_ind and \
# old                len(group_counts) == len(groups):
            if max(group_counts) >= min_ind:
                skimmed_dict[i] = temp_dict[i]
    print "Number of SNPs analysed:", len(snp_dict)
    print "Number of good SNPs:", len(skimmed_dict)
    return(skimmed_dict)

def output_results(snps, out_file, groups, alpha):
    """Write results to file
    """
    with open(out_file, "w") as f:
        group_headers = []
        for i in range(len(groups)):
            group_headers += ["Freq_1", "Freq_2", "Fold_change",
                             "P_value", "Summary"]
        group_headers = "\t".join(group_headers)
        f.write("\t".join(["Contig_pos", "Allel_1", "Allel_2", 
                "Freq_1", "Freq_2", "Fold_change", "P_value",
                group_headers,
                "Global_summary"]) + "\n")
        for loc in sorted(snps):
            allels = snps[loc][0][2:4]
            loc_results = [loc, allels[0], allels[1]]
            glob_freqs = count_variants(snps[loc])
            loc_results += glob_freqs
            glob_fold_change = float(glob_freqs[0]) / glob_freqs[1]
            loc_results.append(glob_fold_change)
            glob_p_value = binom_test([glob_freqs[0], glob_freqs[1]])
            loc_results.append(glob_p_value)
            glob_synthesis = categorize_fold_change(glob_fold_change, 
                                                    glob_p_value, alpha)
            for g in groups:
                pass
                individuals = [x for x in snps[loc] if x[0] == g]
                ind_freqs = count_variants(individuals)
                loc_results += ind_freqs
                try:
                    fold_change = float(ind_freqs[0]) / ind_freqs[1]
                except:
                    fold_change = -99
                loc_results.append(fold_change)
                p_value = binom_test([ind_freqs[0], ind_freqs[1]])
                loc_results.append(p_value)
                synthesis = categorize_fold_change(fold_change, p_value, alpha)
#                print
#                print loc
#                print fold_change, p_value, synthesis
                glob_synthesis += synthesis
                stat = [0, 0, len(individuals)]
                for i in individuals:
                    a = genotype(i)
#                    print a, categorize_fold_change(a.fold_change, a.p_value, alpha)
                    if categorize_fold_change(a.fold_change, a.p_value, 
                        alpha) == synthesis:
                        stat[1] += 1
                    elif categorize_fold_change(a.fold_change, a.p_value,
                        alpha) == categorize_fold_change(fold_change, 1, alpha):
                        stat[0] += 1
                synthesis += str("%i/%i/%i" % (stat[0], stat[1], stat[2]))
                loc_results.append(synthesis)
            loc_results.append(glob_synthesis)
            tabulated_results = "\t".join([str(x) for x in loc_results])
            f.write(tabulated_results + "\n")

def count_variants(individuals):
    """Return variant frequencies
    """
    freq_1 = sum([int(x[4]) for x in individuals])
    freq_2 = sum([int(x[5]) for x in individuals])
    return [freq_1, freq_2]

def categorize_fold_change(fc, pval, alpha=0.05):
    """Return + - or 0 depending on fold_change and significativity
    """
    res = "0"
    if float(fc) < 1:
        res = "-"
        if float(pval) > alpha:
            res = "<"
    elif float(fc) > 1:
        res = "+"
        if float(pval) > alpha:
            res = ">"
    return res

def sign(val):
    """Return -1 or +1 (zero returns +1)
    """
    return copysign(1, float(val))


# Allelic explore
# Slowly but surely brings you
# Closer to results

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:e:a:", ["help",
            "input=", "output=", "header=", "alpha="])
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
        elif option in ('-a', '--alpha'):
            try:
                alpha = float(value)
            except:
                print "Input Error: alpha level must be a floating point number"
                sys.exit(0)
    try:
        with open(input_file) as test:
            pass
    except:
        print "Input Error: No input file specified or file not found."
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
    
    explore_allelic_imbalance(input_file, output_file, header, alpha)

if __name__ == "__main__":
    main()
