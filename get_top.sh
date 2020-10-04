#!/bin/bash
folder_name=$(basename "$PWD")
cd ..
git shortlog -s -n | head -n "$1" | sed -e 's;[0-9]\+;;' -e 's;^[ \t]*;;' > "$folder_name/data/contributors_$1.txt"
