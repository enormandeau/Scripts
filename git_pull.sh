#!/bin/bash
# Update all git repositories in current folder

find . -maxdepth 1 -type d | \
    grep -vE '^.$' | \
    parallel -k -j20 'echo -ne "## "{}"\n  " && cd {} && git pull'

