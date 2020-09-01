#!/bin/bash
python3 user.py
screen -dmS ITGLog ITGLog

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

rm data/receiver
rm data/sender
rm data/time

echo 'Sending done!'

