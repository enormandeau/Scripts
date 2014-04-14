#!/usr/bin/env python
"""Find microarray loop design with random loops that minimize multiple
connections among groups.

Usage:
    %program num_groups num_loops num_iteration

In Linux, use the following line to get the best design:

./microarray_random_loop_design.py 6 4 10000 | perl -pe 's/^\[//; s/\]$//; s/, \[/\t[/g; s/\[+/[/g; s/\]+/]/g' | sort -nr | tail -1

"""
import sys
from itertools import permutations as perm
from random import sample

try:
    ntotal = int(sys.argv[1])
    nwanted = int(sys.argv[2])
    maxiter = int(sys.argv[3])
except:
    print __doc__
    sys.exit(1)

# Generate list of all possible permutations
l = list(perm(xrange(1, ntotal+1)))
l = [list(x) + [x[0]] for x in l]

# Subsample and calculate number of connections among groups
results = []
for i in xrange(maxiter):
    x = sample(l, nwanted)
    c = []
    for i in xrange(ntotal):
        temp = []
        for j in xrange(ntotal):
            temp.append(0)
        c.append(temp)
    for i in x:
        for j in xrange(len(i) - 1):
            a, b = i[j] - 1, i[j+1] - 1
            c[a][b] += 1
            c[b][a] += 1
    results.append([c, x])

# Format and print results
for r in results:
    for i in xrange(len(r[0])):
        for j in xrange(len(r[0][i])):
            if r[0][i][j] == 1:
                r[0][i][j] = 0
            else:
                r[0][i][j] = r[0][i][j] ** 2
    r[0] = sum([sum(x) for x in r[0]])
    print r

