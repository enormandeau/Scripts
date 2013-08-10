#!/bin/bash
# Update all git repositories in current folder

find . -maxdepth 1 -type d | \
    grep -vE '^.$' | \
    parallel 'echo -ne "## "{}"\n  " && cd {} && git pull'

