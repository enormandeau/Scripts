FILE=amdc_contigs_min200.fa.good

# Get repeats with mreps
./mreps -res 3 -exp 3.0 -minsize 24 -maxsize 80 -minperiod 2 -maxperiod 4 -fasta $FILE > $FILE.repeats

# Use mreps_format1.py
mreps_preformat.py $FILE.repeats > $FILE.formated

# Use mreps_format.py to create nice output
mreps_format.py $FILE.formated $FILE $FILE.annot $FILE.annotated

