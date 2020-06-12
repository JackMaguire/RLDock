#!/bin/bash

tag="narrowness"

python3 print_all_optimizers.py | while read opt; do
    # 1 day, 0 hours
    # 1000 MB (1 GB)
    # output file
    sbatch -t "1-0" -n 1 --mem-per-cpu=1000 -o $tag.$opt.log dummy.sh python3 test_narrowness.py --opt $opt
    break
done
