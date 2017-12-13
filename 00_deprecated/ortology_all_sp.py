#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Quick and dirty script to find ortologous genes among many species
# WARNING! Works only under Linux

__authors__ = "Eric Normandeau"
__program_name__ = "ortology_all_sp"
__version_info__ = ('0', '0', '2')
__version__ = '.'.join(__version_info__)
__revision_date__ = "2010-04-21"


# Importing modules

import os
import re
import math
from collections import defaultdict


# Class definitions

class AutoDict(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


# Function definitions

def readfasta(sp_name, re_pattern):
    """Read FASTA file, build dictionary of names pointing to sequences"""
    out = {}
    with open(sp_name + ".fa") as f:
        for line in f:
            if line.startswith(">"):
                contig_name = re.findall(re_pattern, line)
                if len(contig_name) > 0:
                    contig_name = sp_name + "_" + contig_name[0]
                else:
                    contig_name = "NoNameFound"
                contig_seq = ""
                out[contig_name] = contig_seq
            else:
                out[contig_name] += line.rstrip()
    return out

def build_orto_dict(central_sp, other_sp, central_n, other_n):
    """Build complex, multi level ortolog genes dictionary for many species"""
    d = AutoDict()
    for sp in other_sp:
        filename1 = central_sp + "_" + sp + ".txt"
        filename2 = sp + "_" + central_sp + ".txt"
        with open(filename1) as f1:
            with open(filename2) as f2:
                for line in f1:
                    ids = []
                    first_id = re.findall(central_n, line)
                    if len(first_id) > 0:
                        ids.append(central_sp + "_" + first_id[0])
                    second_id = re.findall(other_n, line)
                    if len(second_id) > 0:
                        ids.append(sp + "_" + second_id[0])
                    if len(ids) == 2:
                        d[central_sp][sp][ids[0]] = ids[1]
                for line in f2:
                    ids = []
                    first_id = re.findall(other_n, line)
                    if len(first_id) > 0:
                        ids.append(sp + "_" + first_id[0])
                    second_id = re.findall(central_n, line)
                    if len(second_id) > 0:
                        ids.append(central_sp + "_" + second_id[0])
                    if len(ids) == 2:
                        d[sp][central_sp][ids[0]] = ids[1]
    return d

def check_ortology(a_dict, central_sp, other_sp):
    """Use build_ortolog_dict dictionary to determine ortology."""
    d = defaultdict(list)
    ortologous_count = 0
    for sp in other_sp:
        for id1 in a_dict[central_sp][sp].keys():
            id2 = a_dict[central_sp][sp][id1]
            if a_dict[sp][central_sp][id2] == id1:
                ortologous_count += 1
                d[id1].append(id2)
    print "There are", ortologous_count, "ortologous relationships"
    return d

def reduce_ortologue_dict(a_dict, min_orto):
    """Keep only genes for which there is a minimum number of ortologues."""
    d = defaultdict(list)
    for i in a_dict:
        if len(a_dict[i]) >= min_orto:
            d[i] = a_dict[i]
    print "With a mimimum of", min_orto, "ortologues, we keep", \
          len(d.keys()), "genes."
    return d

def export_table(d, central_sp, other_sp):
    """Write presence/absence table of ortology for each species to a file."""
    with open("ortology_table.txt", "w") as f:
        f.write(central_sp)
        for sp in other_sp:
            f.write("\t" + sp)
        f.write("\n")
        for gene in sorted(d):
            gene_re = re.compile("[A-Z]{2,}[0-9]+\.*[0-9]*")
            gene_id = re.findall(gene_re, gene)[0]
            f.write(gene_id)
            for sp in other_sp:
                presence = 0
                for ortolog in d[gene]:
                    if ortolog.find(sp + "_") > -1:
                        presence = 1
                f.write("\t" + str(presence))
            f.write("\n")

def complement(seq):
    """Return the complement of a sequenc *NOT* it's reverse complement"""
    if not seq.isalpha():
        print "The sequence contained non-alphabetic characters"
        print seq
    if not seq.isupper():
        print "The sequence contained non capital-letter characters"
        seq = seq.upper()
    return seq.replace("A","t").replace("T","a").replace("C","g").replace("G","c").upper()

def reverse_complement(seq):
    return complement(seq)[::-1]

def correct_sense(s1, s2):
    """Insure s2 is in the same sense as s1 for alignment"""
    len_word = 11
    min_ratio = 2
    s2_rev = reverse_complement(s2)
    score_sense = 1
    score_anti = 1
    for i in range(len(s1) - len_word + 1):
        word = s1[i:i + len_word]
        if s2.find(word) > -1:
            score_sense +=1
        if s2_rev.find(word) > -1:
            score_anti +=1
    ratio = math.log(float(score_sense) / score_anti, 10)
    correct_seq = s2
    if ratio < - math.log(min_ratio, 10):
        correct_seq = s2_rev
    return correct_seq

def export_sequences(d_central, central_sp, other_sp, central_n, other_n):
    central_sp_seqs = readfasta(central_sp, central_n)
    out_folder = "ortology_results_all_species"
    out_file = central_sp + "_ortologs.txt"
    out_path = os.path.join(out_folder, out_file)
    try:
        with open (out_path, "w") as test:
            pass
    except:
        print "Created", "'"+ out_folder +"'", "folder to put result files in"
        os.mkdir(out_folder)
    with open(out_path, "w") as f:
        d_other = {}
        for sp in other_sp:
            d_other.update(readfasta(sp, other_n))
        for k1 in sorted(d_central.keys()):
            f.write(">" + k1 + "_" + k1 + "\n")
            seq1 = central_sp_seqs[k1][:]
            f.write(seq1 + "\n")
            longeur_seq = len(seq1)
            for sp in other_sp:
                found_sp = False
                for contig in d_central[k1]:
                    if contig.find(sp) > -1:
                        found_sp = True
                        seq2 = d_other[contig][:]
                        seq2 = correct_sense(seq1, seq2)
                        f.write(">" + k1 + "_" + contig + "\n")
                        f.write(seq2 + "\n")
                if found_sp == False:
                    f.write(">" + k1 + "_" + sp + "_no_contig" + "\n")
                    f.write("ATG" + "\n") # Trick so that Muscle keeps the seq


# Pseudo main

central_species = "salmo"
other_species = "coreg danio esoxl mykis namay salve".split()
#other_species = "coreg mykis namay salve".split()

central_name = re.compile("[A-Z]{2,}[0-9]+\.*[0-9]*")
other_names = re.compile("_(Contig_[0-9]+)")

MIN_SP = 3

my_dict = build_orto_dict(central_species, other_species, central_name, other_names)
orto_genes = check_ortology(my_dict, central_species, other_species)
reduced_orto = reduce_ortologue_dict(orto_genes, MIN_SP)
print "Writing result files"
export_table(reduced_orto, central_species, other_species)
export_sequences(reduced_orto, central_species, other_species, central_name, other_names)

