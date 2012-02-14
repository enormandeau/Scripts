#!/usr/bin/env bash

# Resize terminal window to $1 lines and $2 columns
# Use: ./resize_term.sh <nrow> <ncol>

# positive integer test (including zero)
function positive_int() { return $(test "$@" -eq "$@" > /dev/null 2>&1 && test "$@" -ge 0 > /dev/null 2>&1); }

# resize the Terminal window
function sizetw() { 
   if [[ $# -eq 2 ]] && $(positive_int "$1") && $(positive_int "$2"); then 
      printf "\e[8;${1};${2};t"
      return 0
   fi
   return 1
}

# the default Terminal window size: 26 lines and 107 columns
sizetw $1 $2

