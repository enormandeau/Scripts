#!/bin/bash
# Monitor progress of tasks in the terminal with progress_bar.py

while sleep 1
    do clear
    top -n 1 | head -15
    echo ""
    echo "Processes:"
    # Insert processes to monitor here following the example below:
    # progress_bar.py `ls -1 all_samples/*.fa | wc -l` `ls -1 analyzed/*.fa 2>/dev/null | wc -l` Analysis
    sleep 59
done

