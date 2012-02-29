# Class examples

class myNum():
    def __init__(self, n):
        self.num=n
    def __str__(self):
        return str("Number: %i %i" % (self.num, self.num ** 2))

class fasta():
    def __init__(self, n, s):
        self.n = n
        self.s = s
    def __str__(self):
        return str(">%s\t%s" % (self.n, self.s[0:31]))
    def __add__(self, s2):
        res = fasta("", "")
        res.n = self.n + s2.n
        res.s = self.s + s2.s
        return res
    def lower(self):
        self.s = self.s.lower()

class fasta_parser():
    def __init__(self, filename):
        self.f = filename
        self.sequences = []
        with open(self.f) as in_file:
            for line in in_file:
                l = line.strip()
                if l != "":
                    if l.startswith(">"):
                        self.sequences.append(fasta(l.replace(">", ""), ""))
                    else:
                        self.sequences[-1].s += l
    def __str__(self):
        for s in self.sequences:
            print s


seqs = []
seqs.append(fasta("Seq1", "CGTGTGCGTGTGCCAAACG"))
seqs.append(fasta("Seq2", "ACACACACACACAC"))
seqs.append(fasta("Seq3", "TGACTGACAACCACGGACGACG"))

# each of these sequences is an object, that means an instance of type 'fasta'

