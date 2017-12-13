#!/bin/bash
# Kill any 'mpg123' running processes
tokill=`ps aux | grep mpg123 | grep -v grep | awk '{print $2}'`
for i in $tokill; do kill $i; done
