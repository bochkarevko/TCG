#!/bin/bash
folder_name=$(basename "$PWD")
cd ..
git log --author="$1" --name-only | sed -e '/^commit/d' -e '/^Author/d' -e "/^Date*/d" -e '/^$/d' -e '/^\s/d' | sort --unique > "$folder_name/data/$1.txt"
