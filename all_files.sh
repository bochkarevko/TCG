#!/bin/bash
tr '\n' '\0' <data/contributors_$1.txt | xargs -n 1 -0 ./contributor_files.sh 
