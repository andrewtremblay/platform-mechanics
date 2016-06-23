#!/bin/bash
# runs a script when a directory changes
# requires the following for Mac OS:
# pip3 install watchdog
# brew install libyaml

watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command="./relaunchGame.sh" \
    .
