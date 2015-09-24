#!/bin/bash
# Example of script backup
TIMESTAMP=$(date +%Y-%m-%d_%Hh%Mm%Ss)

echo "Hello $1"

# Copy script as it was run
LOG_FOLDER="logfiles"
SCRIPT=$0
NAME=$(basename $0)
mkdir $LOG_FOLDER 2> /dev/null

cp $SCRIPT $LOG_FOLDER/"$TIMESTAMP"_"$NAME"

