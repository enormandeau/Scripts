#!/usr/bin/env python
"""Average RNA-Seq data by unique genes usign a column with unique gene
identifiers from a tab separated file with the data of one sequence per line.

Usage:
    ./rna_seq_average_by_gene.py  input_file  id_column  name_col  data_column

id_column: Number of the column containing the identifiers of the unique genes.
    When multiple lines share the same identifier, their data are combined

name_col: Number of the column containing the sequence names.

data_column: Number of the first column containing the data. All
    subsequent columns are expected to contain data.
"""

# Importing modules
import sys

# Parsing user input
try:
    input_file = sys.argv[1]
    id_col = int(sys.argv[2]) - 1
    name_col = int(sys.argv[3]) - 1
    data_col = int(sys.argv[4]) - 1
except:
    print __doc__
    sys.exit(1)

# Main
if __name__ == '__main__':
    data = [x.strip().split("\t") for x in open(input_file).readlines() if x.strip() != ""]
    unique_genes = list(set([x[id_col] for x in data]))
    with open(input_file + ".unique", "w") as f1:
        with open(input_file + ".groups", "w") as f2:
            for gene in unique_genes:
                #print "---------" + gene + "---------"
                gene_names = [x[name_col] for x in data if x[id_col] == gene]
                gene_data = [x[data_col:] for x in data if x[id_col] == gene]
                nseq = len(gene_data)
                nind = len(gene_data[0])
                avg = [0] * nind
                for i in xrange(nind):
                    ind_data = [int(x[i]) for x in gene_data]
                    avg[i] = sum(ind_data) / float(nseq)
                f1.write(gene + "\t" + "\t".join([str(x) for x in avg]) + "\n")
                f2.write(gene + "\t" + "\t".join(gene_names) + "\n")
