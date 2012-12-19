#!/usr/bin/python
"""Compare SNP presence between the UNEAK pipeline and the IBIS pipeline outputs.

Usage:
    compare_uneak_vs_ibis.py uneak_fasta uneak_sam standard_vcf
    
"""

# Importing modules
import sys
import re
from collections import defaultdict

try:
    from Bio import SeqIO
except:
    print "This program requires the Biopython library"
    sys.exit(0)

# Defining functions
def find_snp_position(s1, s2):
    assert len(s1) == len(s2), "Sequences have different lengths"
    snps = []
    for i in xrange(len(s1)):
        if s1[i] != s2[i]:
            snps.append(i + 1)
    assert len(snps) > 0, "No SNP found"
    assert len(snps) <= 1, "More than one SNP found"
    return snps[0]


if __name__ == "__main__":
    try:
        uneak_fasta_file = open(sys.argv[1], "rU")
        uneak_sam_file = open(sys.argv[2], "rU")
        #standard_vcf_file = open(sys.argv[3], "rU")
    except:
        print __doc__
        sys.exit(1)
    
    #output_counts = open("OUTPUT_counts.txt", "w")
    output_not_mapped = open("OUTPUT_not_mapped.txt", "w")
    output_mapped_all = open("OUTPUT_mapped_all.txt", "w")
    output_mapped_both = open("OUTPUT_mapped_both.txt", "w")
    output_mapped_one = open("OUTPUT_mapped_one.txt", "w")
    output_mapped_different_positions = open("OUTPUT_mapped_different_positions.txt", "w")
    output_mapped_multiple = open("OUTPUT_mapped_multiple.txt", "w")
    #output_common = open("OUTPUT_common.txt", "w")
    #output_common_multiple = open("OUTPUT_common_multiple.txt", "w")
    #output_only_uneak = open("OUTPUT_only_uneak.txt", "w")
    #output_only_vcf = open("OUTPUT_only_vcf.txt", "w")
    
    ## Treating fasta file
    # Build dictionary of sequences, query and hits
    fasta_dict = defaultdict(dict)
    for seq in SeqIO.parse(uneak_fasta_file, "fasta"):
        basename, hit_or_query = seq.name.split("_")
        fasta_dict[basename][hit_or_query] = seq.seq.tostring()
    
    # For each Query-Hit couple, find the position of the SNP and add to fasta_dict
    for locus in fasta_dict.keys():
        if len(fasta_dict[locus]) == 2:
            s1 = fasta_dict[locus]["query"]
            s2 = fasta_dict[locus]["hit"]
            fasta_dict[locus]["snp_offset"] = find_snp_position(s1, s2)
    
    ## Treating sam file
    sam_dict = defaultdict(dict)
    for line in uneak_sam_file.readlines():
        if not (line.startswith("@") or line.strip() == ""):
            l = line.strip().split("\t")
            seq = l[0]
            basename, hit_or_query = seq.split("_")
            direction = int(l[1])
            chromosome = l[2]
            tag_position = int(l[3])
            snp_offset = fasta_dict[basename]["snp_offset"]
            if direction == 0:
                snp_position = tag_position + snp_offset - 1
            elif direction == 16:
                snp_position = tag_position + (64 - snp_offset)
            else:
                snp_position = -99
                chromosome = "no_hit"
            sam_dict[basename][hit_or_query] = {"snp_position":snp_position, "chromosome":chromosome, "direction":direction}
    
    sam_dict_reversed = defaultdict(set)
    for tp in sam_dict:
        if sam_dict[tp]["query"]["snp_position"] != -99:
            ch = sam_dict[tp]["query"]["chromosome"]
            pos = sam_dict[tp]["query"]["snp_position"]
            sam_dict_reversed[(ch, pos)].add(tp)
        if sam_dict[tp]["hit"]["snp_position"] != -99:
            ch = sam_dict[tp]["hit"]["chromosome"]
            pos = sam_dict[tp]["hit"]["snp_position"]
            sam_dict_reversed[(ch, pos)].add(tp)
    
    del fasta_dict
    
    ### Treating standard_vcf_file
    #vcf_dict = defaultdict(list)
    #for line in standard_vcf_file.readlines():
    #    if not (line.startswith("#") or line.startswith("\"") or line.strip() == ""):
    #        l = line.strip().split("\t")
    #        chromosome = l[0]
    #        position = int(l[1])
    #        vcf_dict[chromosome].append(position)
    
    ## Find mapped status of each locus
    mapping_counts = defaultdict(int)    
    chromosome_position_uneak = set()
    for locus in sam_dict:
        category = []
        dir1 = sam_dict[locus]["query"]["direction"]
        chr1 = sam_dict[locus]["query"]["chromosome"]
        pos1 = sam_dict[locus]["query"]["snp_position"]
        dir2 = sam_dict[locus]["hit"]["direction"]
        chr2 = sam_dict[locus]["hit"]["chromosome"]
        pos2 = sam_dict[locus]["hit"]["snp_position"]
        status = ""
            
        if pos1 == -99 and pos2 == -99:
            category.append("notMapped")
            output_not_mapped.write(locus + "\n")
        elif pos1 == -99 or pos2 == -99:
            category.append("onlyOneMapped")
            if pos1 != -99:
                chromosome_position_uneak.add((chr1, pos1))
                output_mapped_one.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\n")
                output_mapped_all.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\t" + "onlyOneMapped" + "\n")
            else:
                chromosome_position_uneak.add((chr2, pos2))
                output_mapped_one.write(locus + "\t" + chr2 + "\t" + str(pos2) + "\n")
                output_mapped_all.write(locus + "\t" + chr2 + "\t" + str(pos2) + "\t" + "onlyOneMapped" + "\n")
        else:
            if pos1 == pos2:
                category.append("bothMapped")
                chromosome_position_uneak.add((chr1, pos1))
                output_mapped_both.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\t" + "BothMapped" + "\n")
                output_mapped_all.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\t" + "BothMapped" + "\n")
            else:
                category.append("differentPosition")
                chromosome_position_uneak.add((chr1, pos1))
                chromosome_position_uneak.add((chr2, pos2))
                output_mapped_different_positions.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\t" + chr2 + "\t" + str(pos2) + "\n")
                output_mapped_all.write(locus + "\t" + chr1 + "\t" + str(pos1) + "\t" + "differentPositions" + "\n")
                output_mapped_all.write(locus + "\t" + chr2 + "\t" + str(pos2) + "\t" + "differentPositions" + "\n")

        mapping_counts["_".join(category)] += 1
    
## Creating uneak_mapped_nonredondant_file
    #uneak_dict = defaultdict(list)
    #for ch_pos in list(chromosome_position_uneak):
    #    ch, pos = ch_pos
    #    uneak_dict[ch].append(pos)
   # 
    #for chromosome in uneak_dict:
    #    for position in uneak_dict[chromosome]:
    #        if position not in vcf_dict[chromosome]:
    #            output_only_uneak.write(chromosome + "\t" + str(position) + "\n")
    #        else:
    #            output_common.write(chromosome + "\t" + str(position) + "\n")
    #            output_common_multiple.write(chromosome + "\t" + str(position) +
    #                "\t" + "\t".join(list(sam_dict_reversed[(chromosome, position)])) + "\n")
   # 
    #for chromosome in vcf_dict:
    #    for position in vcf_dict[chromosome]:
    #        if position not in uneak_dict[chromosome]:
    #            output_only_vcf.write(chromosome + "\t" + str(position) + "\n")

    #for k in sorted(mapping_counts):
    #    output_counts.write(k + "\t" + str(mapping_counts[k]) + "\n")
   # 
    for k in sorted(sam_dict_reversed):
        ch, pos = k
        tps = sam_dict_reversed[k]
        output_mapped_multiple.write("\t".join([ch] + [str(pos)] + list(tps)) + "\n")
    
    #output_counts.close()
    output_not_mapped.close()
    output_mapped_all.close()
    output_mapped_both.close()
    output_mapped_one.close()
    output_mapped_different_positions.close()
    output_mapped_multiple.close()
    #output_common.close()
    #output_common_multiple.close()
    #output_only_uneak.close()
    #output_only_vcf.close()








