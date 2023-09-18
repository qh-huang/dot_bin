#!/bin/bash
 
for branch in $(git branch); do                                                             ✔ │ 18m 32s │ base 🐍 │ 23:54:54
    git checkout $branch --force; git reset HEAD --hard; git pull
done
