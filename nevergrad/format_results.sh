#!/bin/bash

for x in narrowness.*.log; do
    tag=$(echo $x | awk -F. '{print $2}')
    echo $tag $(
	grep -A 1000 width_factor $x | grep -v [a-z] | tail -n 8 | while read line; do
	    if [[ `echo $line | awk '{print NF}'` -eq 3 ]]; then
		echo $line
	    fi
	done
    )
done | grep 0
