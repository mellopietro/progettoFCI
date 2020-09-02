#!/bin/bash
python3 user.py
screen -dmS ITGLog ITGLog -q 100

for h in $(cat data/receiver)
do
    h=$(echo $h | tr "_" " ")
    readarray -d '&' -t d <<< "$h"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -dmS ITGRecv ITGRecv"
done
echo 'Receiver ready...'

sleep 2

for h in $(cat data/sender)
do
    readarray -d '%' -t d <<< "$h"
    name=$(echo ${d[0]} | tr "_" " ")
    readarray -d '&' -t n <<< "$name"
    parameters=$(echo ${d[1]} | tr "_" " ")
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "screen -dmS ITGSend ITGSend $parameters"
done

echo 'Sending started...'

time=$(cat data/time)
sleep $time

sleep 2

for h in $(cat data/receiver)
do
    h=$(echo $h | tr "_" " ")
    readarray -d '&' -t d <<< "$h"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -S ITGRecv -X quit"
done

screen -S ITGLog -X quit

echo 'Sending done!'
echo 'Computation started...'

h=$(cat data/number)
for((i=0;i<h;i++))
do
    ITGDec results/send$i.log -d 1000 results/send$i.dat
    ITGDec results/recv$i.log -d 1000 results/recv$i.dat
done

python3 result.py

rm data/receiver
rm data/sender
rm data/time
rm data/hosts
rm results/*



