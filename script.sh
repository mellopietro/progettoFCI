#!/bin/bash

python3 user.py

screen -dmS ITGLog ITGLog

readarray -d '%' -t rec <<< "$(cat data/receiver)"

for ((i=0;i<${#rec[@]}-1;i++))
do
    readarray -d '&' -t d <<< "${rec[$i]}"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -dmS ITGRecv ITGRecv"
done

echo 'Receiver ready...'

sleep 4

on=$(cat data/on)

for i in $on
do
    readarray -d '%' -t s <<< "$(cat data/logInfo${i})"
    readarray -d '&' -t n <<< "${s[0]}"
    readarray -d ' ' -t name <<< "${n[0]}"
    sshpass -p "${n[1]}" scp data/sender$i ${name[0]}:
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "screen -dmS ITGSend ITGSend sender${i} ${s[1]}"
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "rm sender${i}"
done

echo 'Sending started...'

time=$(cat data/time)
sleep $time
sleep 5

readarray -d '%' -t rec <<< "$(cat data/receiver)"

for ((i=0;i<${#rec[@]}-1;i++))
do
    readarray -d '&' -t d <<< "${rec[$i]}"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -S ITGRecv -X quit"
done

screen -S ITGLog -X quit

echo 'Sending done!'


