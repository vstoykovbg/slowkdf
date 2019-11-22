#!/bin/bash

while true; do

date
processID=$(ps a | grep slowkdf | grep python | head -n 1 | cut -d " " -f 1)

echo "Process ID: \"$processID\""

if [ -n "$processID" ] && [ "$processID" -eq "$processID" ] 2>/dev/null; then
  echo "cpulimit -l 50 -p \"$processID\""
  cpulimit -l 50 -p "$processID"
else
  echo "Process not found."
fi

echo "sleeping 1 second..."
sleep 1

done
