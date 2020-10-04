#!/bin/bash
git log --author="$1" --name-only | sed -e '/^commit/d' -e '/^Author/d' -e "/^Date*/d" -e '/^$/d' -e '/^\s/d' | sort --unique > "$1.txt"
