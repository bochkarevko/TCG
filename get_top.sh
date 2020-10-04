#!/bin/bash
git shortlog -s -n | head -n 50 | sed -e 's;[0-9]\+;;' -e 's;^[ \t]*;;' > t50c.txt
