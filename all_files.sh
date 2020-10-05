#!/bin/bash
xargs -n 1 -d '\n' ./contributor_files.sh <data/contributors_$1.txt
