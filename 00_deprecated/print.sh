#! /bin/bash
# Use a remote host connected to a printer to print a document
document=$1
host=$2
cat $document | ssh $host lpr -o sides=two-sided-long-edge

