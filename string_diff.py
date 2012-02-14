#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Return the Levenstein distance between 2 strings.

Not to be used for strings longer then 10 letters.

Usage:
    %program <string_1> <string_2>"""

import sys

try:
    a = sys.argv[1].lower()
    b = sys.argv[2].lower()
except:
    print __doc__
    sys.exit(0)

def lev(a, b):
    if not a: return len(b)
    if not b: return len(a)
    return min(lev(a[1:], b[1:])+(a[0] != b[0]), lev(a[1:], b)+1, lev(a, b[1:])+1)

print "The distance between the following strings is: %i\n%s\n%s" % (lev(a, b), a, b)

