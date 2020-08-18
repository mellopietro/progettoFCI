#!/bin/bash
python3 user.py
screen -dmS ITGLog ITGLog

for h in $(cat data/receiver)
do
    d=$(echo $h | tr "_" " ")
    sshpass -p "123456" ssh -o StrictHostKeyChecking=no $d "screen -dmS ITGRecv ITGRecv"
done
echo 'Receiver ready...'

for h in $(cat data/sender)
do
    h=$(echo $h | tr "%" " ")
    IFS=' '
    read -a d <<< "$h"
    name=$(echo ${d[0]} | tr "_" " ")
    parameters=$(echo ${d[1]} | tr "_" " ")
    sshpass -p "123456" ssh -o StrictHostKeyChecking=no $name "screen -dmS ITGSend ITGSend $parameters"
done
echo 'Sending started...'

time=$(cat data/time)
sleep $time

for h in $(cat data/receiver)
do
    d=$(echo $h | tr "_" " ")
    sshpass -p "123456" ssh $d "screen -S ITGRecv -X quit"
done

screen -S ITGLog -X quit

rm data/receiver
rm data/sender
rm data/time

echo 'Sending done!'

