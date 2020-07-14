#!/bin/bash

round="1"
while true; do
    num_of_jobs_pending=$(squeue -u ivyy0201 | grep PD | wc -l)
    if [[ $num_of_jobs_pending -lt "2" ]]; then
	for opt in "RealSpacePSO" "MEDA" "DoubleFastGADiscreteOnePlusOne" "NaiveTBPSA" "CMA" "DiscreteOnePlusOne" "RecMutDE"; do
	    sbatch submit.sh $opt $round
	done
	round=$((round+1))
    fi

    sleep 60 #sleep for 60 seconds, 1 minute
done
