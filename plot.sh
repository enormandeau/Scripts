#!/bin/bash
gnuplot -p -e "set nokey; plot './$1'; pause -1"
