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
    rm data/logInfo${i} data/sender${i}
    sshpass -p "${n[1]}" ssh -o StrictHostKeyChecking=no ${n[0]} "rm sender${i}"
done

echo 'Sending started...'

readarray -d ' ' -t time <<< "$(cat data/time)"
sleep ${time[0]}
sleep 5

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
    ITGDec results/recv$i.log -${time[2]} ${time[1]} results/recv$i.dat > /dev/null 2>&1
done

python3 result.py

rm data/receiver
rm data/time
rm data/hosts
rm data/on
rm results/*.dat
