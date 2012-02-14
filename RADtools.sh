#!/usr/bin/env bash

# RADtools scripts and use

clear

echo 'Using the RADtools pipeline'
echo '---------------------------'
echo
echo 'RADpools in use...'
echo

output_file="coregonus_m4f_m1q20r2_t0m2i.txt"

time RADpools --in ../../s_1_sequence.txt --species coregonus -m 4 -f
# -v (verbose)
# -m (num. cores)
# -q (min. base quality)
# -f (fuzzy mid match)

echo 'Done'
echo
echo 'RADtags in use...'

time RADtags -e 10000 -s coregonus -m 1 -q 20 -r 2
# -m (num. cores)
# -q (min. base qual.)
# -r (min. num. reads per tag)

echo 'Done'
echo
echo 'RADmarkers in use...'

time RADmarkers -s coregonus -t 0 -m 2 -i >$output_file
# -o (output SNPs)
# -t (rem. tags w/ less than n num. of reads in each pools)
# Number of reads across pools is crucial!
# -m (acceptable num. of mismatches across pools to join into clusters, <= 3)

pwd
echo 'Done'
echo
echo "Summary has been written to file: $output_file"
grep "^[0-9]" coregonus_vm4f_m1q20r2_t0m2i.txt | sed 's/M//g' >$output_file
echo '----------- End -----------'
