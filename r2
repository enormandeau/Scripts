#!/usr/bin/env bash
# Resize the terminal window

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
sizetw 28 132
