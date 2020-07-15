#!/bin/bash

if [[ "$#" -ne 1 ]]; then
    echo "You forgot to pass the rank as argument number 1"
    exit 1
fi

#1, 5, 10, 25, 50, etc
rank=$1

while read combination; do
   
    for dir in $combination; do
	grep pose $dir/*.pdb | awk '{print $NF}'
    done | sort -g | head -n $rank | tail -n 1
    
done
