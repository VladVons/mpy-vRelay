#!/bin/bash


rm wget-log.*

for i in {1..25}; do
    echo "i: $i"
    xfce4-terminal --hold --geometry=10x10 --command="./wget.sh"
done
