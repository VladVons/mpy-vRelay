#!/bin/bash


rm wget-log.*

for i in {1..20}; do
    echo "i: $i"
    xfce4-terminal --hold --geometry=12x12 --command="./wget.sh"
done
