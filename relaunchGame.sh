#!/bin/bash
ps -ef | grep 'src/main.py' | awk '{print $2}' | xargs kill 1>&- 2>&-
echo "***********************"
echo "Relaunching from script"
echo "***********************"
python3 src/main.py
