#!/bin/bash

while read combination; do
    
    best_score="9999999999"
    for dir in $combination; do
	#echo $dir
	score=$(grep pose $dir/*.pdb | awk '{print $NF}' | sort -g | head -n1 )
	if [[ $score -lt $best_score ]]; then
	    best_score=$score
	fi
    done
    echo $best_score
    
done
