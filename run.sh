#!/bin/sh
for input in $1/input*; do
    echo $input
    python $1/s.py < $input
done
