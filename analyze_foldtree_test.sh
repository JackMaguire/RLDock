#!/bin/bash

tag="centroid"
opt="RealSpacePSO"

for x in {1..10000}; do
    echo $x $(
	for y in longleaf_run_*; do
	    grep XYZ $y/$tag.$opt.log | head -n $x | awk '{print $2}' | awk 'min=="" || $1 < min {min=$1} END {print min}'
	done
	 )
done
