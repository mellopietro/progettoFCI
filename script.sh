#!/bin/bash
python3 user.py
screen -dmS ITGLog ITGLog

for h in $(cat data/receiver)
do
    d=$(echo $h | tr "_" " ")
    IFS='&'
    read -a d <<< "$d"
    sshpass -p "${d[1]}" ssh -o StrictHostKeyChecking=no ${d[0]} "screen -dmS ITGRecv ITGRecv"
done
echo 'Receiver ready...'

sleep 2

for h in $(cat data/sender)
do
    h=$(echo $h | tr "%" " ")
    IFS=' '
    read -a d <<< "$h"
    name=$(echo ${d[0]} | tr "_" " ")
    IFS='&'
    read -a name <<< "$name"
    parameters=$(echo ${d[1]} | tr "_" " ")
    sshpass -p "${name[1]}" ssh -o StrictHostKeyChecking=no ${name[0]} "screen -dmS ITGSend ITGSend $parameters"
done

echo 'Sending started...'

time=$(cat data/time)
sleep $time

sleep 2

for h in $(cat data/receiver)
do
    d=$(echo $h | tr "_" " ")
    IFS='&'
    read -a d <<< "$d"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -S ITGRecv -X quit"
done

screen -S ITGLog -X quit

rm data/receiver
rm data/sender
rm data/time

echo 'Sending done!'

