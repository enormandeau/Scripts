#!/usr/bin/env python
"""Print a progress bar given a total and a current progress

USAGE:
    %program completed total [process_name]

EXAMPLE:
    progress_bar.py 17 30 Testing

gives:
    Test:           17/30   (=================             ) 56.7%
"""
import sys
import math

try:
    number_completed = float(sys.argv[1])
    number_total = float(sys.argv[2])
except:
    print(__doc__)
    sys.exit(1)

assert number_completed <= number_total, "completed must be smaller or equal than total"
try:
    process_name = sys.argv[3]
except:
    process_name = "progress"

try:
    percent_completed = 100. * number_completed / number_total
except:
    percent_completed = 0

name = process_name + ": "
name = name + (16 - len(name)) * " "

# Print integers without .0
if number_completed//1 == number_completed and number_total//1 == number_total:
    numbers = str(int(number_completed)) + "/" + str(int(number_total)) + " "
else:
    numbers = str(number_completed) + "/" + str(number_total) + " "

numbers = numbers + (8 - len(numbers)) * " "

progress = int(math.floor(percent_completed * 0.3)) * "="
progress = progress + (30 - len(progress)) * " "
progress = "(" + progress + ") "

percent = str("%3.1f" % percent_completed) + "%"

print(name + numbers + progress + percent)
