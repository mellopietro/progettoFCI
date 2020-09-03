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

sleep 2

on=$(cat data/on)

for i in $on
do
    readarray -d '%' -t s <<< "$(cat data/logInfo${i})"
    readarray -d '&' -t n <<< "${s[0]}"
    readarray -d ' ' -t name <<< "${n[0]}"
    sshpass -p "${n[1]}" scp data/sender$i ${name[0]}:/home/pietromello
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "screen -dmS ITGSend ITGSend sender${i} ${s[1]}"
    rm data/logInfo${i} data/sender${i}
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "rm sender${i}"
    
done

echo 'Sending started...'

time=$(cat data/time)
sleep $time

sleep 2

readarray -d '%' -t rec <<< "$(cat data/receiver)"

for ((i=0;i<${#rec[@]}-1;i++))
do
    readarray -d '&' -t d <<< "${rec[$i]}"
    sshpass -p "${d[1]}" ssh ${d[0]} "screen -S ITGRecv -X quit"
done

screen -S ITGLog -X quit

echo 'Sending done!'
echo 'Computation started...'

for i in $on
do
    #ITGDec results/send$i.log -d 1000 results/send$i.dat
    ITGDec results/recv$i.log -b 1000 results/recv$i.dat
done

#python3 result.py

rm data/receiver
rm data/time
rm data/hosts
rm data/on

#rm results/*
