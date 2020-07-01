#!/bin/bash

for x in {118..134}; do
    cp -r longleaf_template longleaf_run_$x
    cd longleaf_$x
    bash submit_centroid.sh
    cd ../
done
