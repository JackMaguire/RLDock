#!/bin/bash

dir=$1
if [ -d $dir ]; then
    grep pose $dir/*.pdb | awk '{print $1 " " $NF}' | sort -gk2
else
    echo "directory \"$dir\" not found"
fi
