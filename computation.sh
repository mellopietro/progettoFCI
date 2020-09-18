#!/bin/bash

echo 'Computation started...'

on=$(cat data/on)

for i in $on
do
    ITGDec results/recv$i.log > results/recv$i.txt
done

python3 result.py

echo 'Computation done!!'