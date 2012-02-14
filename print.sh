#! /bin/bash
# Use a remote host connected to a printer to print a document
cat $1 | ssh labolb@132.203.89.166 lpr -o sides=two-sided-long-edge
