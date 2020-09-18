import numpy as np
import pandas as pd


def firstNumPos(frase,string):
    i = string.index(frase)
    while True:
        if string[i].isdigit() == True:
            return i
        i = i + 1


while True:
    try: 
        file = open('data/hosts','r')
        name = file.read()
        file.close()
    except:
        name = input('Input the path of the host file: ')
    try:
        file = open(name,'r')
        group = file.read()
        file.close()
        if('host_file' in group):
            break
        print('Can\'t find file, try again')
    except:
        print('Can\'t find file, try again')
    
g = group[group.index('\n')+1:]
users = g.split('\n')
users = users[0:-1]

for i in range(len(users)):
    users[i]=users[i][users[i].index('@')+1:users[i].index(' ')]

rA = []
index = []
column = []
lMax = 0

file = open('data/on','r')
val = file.read()
file.close()

n = []
sender = []
receiver = []
totalTime = []
totalPack = []
minDelay = []
maxDelay = []
avgDelay = []
avgJitter = []
stdDelay = []
byte = []
bitrate = []
packrate = []
dropped = []
loss = []

for i in val:
    try:
        i = int(i)
        file = open('results/recv'+str(i)+'.txt')
        recv = file.read()
        file.close()
        
        while True:
            if recv.find('Flow number:') == -1:
                break
            recv = recv[firstNumPos('Flow number:',recv):]
            n.append(int(1))
            recv = recv[firstNumPos('From',recv):]
            receiver.append(recv[:recv.index(':')])
            recv = recv[firstNumPos('To',recv):]
            sender.append(recv[:recv.index(':')])
            recv = recv[firstNumPos('Total time',recv):]
            totalTime.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Total packets',recv):]
            totalPack.append(int(recv[:recv.index('\n')]))
            recv = recv[firstNumPos('Minimum delay',recv):]
            minDelay.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Maximum delay',recv):]
            maxDelay.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Average delay',recv):]
            avgDelay.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Average jitter',recv):]
            avgJitter.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Delay standard deviation',recv):]
            stdDelay.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Bytes received',recv):]
            byte.append(int(recv[:recv.index('\n')]))
            recv = recv[firstNumPos('Average bitrate',recv):]
            bitrate.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Average packet rate',recv):]
            packrate.append(float(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Packets dropped',recv):]
            dropped.append(int(recv[:recv.index(' ')]))
            recv = recv[firstNumPos('Average loss-burst size',recv):]
            loss.append(float(recv[:recv.index(' ')]))
    except:
        continue

num = len(n)
n.append(int(-1))
sender.append(int(0))
receiver.append(int(0))
totalTime.append(int(0))
totalPack.append(int(0))
minDelay.append(int(0))
maxDelay.append(int(0))
avgDelay.append(int(0))
avgJitter.append(int(0))
stdDelay.append(int(0))
byte.append(int(0))
bitrate.append(int(0))
packrate.append(int(0))
dropped.append(int(0))
loss.append(int(0))

for s in users:
    for r in users:
        n.append(int(0))
        sender.append(s)
        receiver.append(r)
        totalTime.append(int(0))
        totalPack.append(int(0))
        minDelay.append(int(0))
        maxDelay.append(int(0))
        avgDelay.append(int(0))
        avgJitter.append(int(0))
        stdDelay.append(int(0))
        byte.append(int(0))
        bitrate.append(int(0))
        packrate.append(int(0))
        dropped.append(int(0))
        loss.append(int(0))
        i = 0
        while True:
            if n[i] == -1:
                break
            if s == sender[i] and r == receiver[i]:
                j = len(n)-1
                num = num - 1
                n[j] = n[j] + 1
                totalTime[j] = max(totalTime[j],totalTime[i])
                totalPack[j] = totalPack[j] + totalPack[i]
                minDelay[j] = min(minDelay[j],minDelay[i])
                maxDelay[j] = max(maxDelay[j],maxDelay[i])
                avgDelay[j] = ((n[j]-1)*avgDelay[j]+avgDelay[i])/n[j]
                avgJitter[j] = ((n[j]-1)*avgJitter[j]+avgJitter[i])/n[j]
                stdDelay[j] = ((n[j]-1)*stdDelay[j]+stdDelay[i])/n[j]
                byte[j] = byte[j] + byte[i]
                bitrate[j] = ((n[j]-1)*bitrate[j]+bitrate[i])/n[j]
                packrate[j] = ((n[j]-1)*packrate[j]+packrate[i])/n[j]
                dropped[j] = dropped[j] + dropped[i]
                loss[j] = ((n[j]-1)*loss[j]+loss[i])/n[j]
                n.pop(i)
                sender.pop(i)
                receiver.pop(i)
                totalTime.pop(i)
                totalPack.pop(i)
                minDelay.pop(i)
                maxDelay.pop(i)
                avgDelay.pop(i)
                avgJitter.pop(i)
                stdDelay.pop(i)
                byte.pop(i)
                bitrate.pop(i)
                packrate.pop(i)
                dropped.pop(i)
                loss.pop(i)
            else:
                i = i + 1
i = 0
num = len(n)
while True:
    if i >= num:
        break
    if n[i]<=0:
        n.pop(i)
        sender.pop(i)
        receiver.pop(i)
        totalTime.pop(i)
        totalPack.pop(i)
        minDelay.pop(i)
        maxDelay.pop(i)
        avgDelay.pop(i)
        avgJitter.pop(i)
        stdDelay.pop(i)
        byte.pop(i)
        bitrate.pop(i)
        packrate.pop(i)
        dropped.pop(i)
        loss.pop(i)
        num = num - 1
    else: 
        i = i + 1
             
data = {'Number': n,'Sender': sender, 'Receiver': receiver, 'Total Time': totalTime, 'Total packets': totalPack, 
'Minimum delay': minDelay, 'Maximum delay': maxDelay, 'Average delay': avgDelay, 'Average jitter': avgJitter, 
'Delay standard deviation': stdDelay, 'Bytes received': byte, 'Average bitrate': bitrate, 'Average packet rate': packrate, 
'Packets dropped': dropped, 'Average loss-burst size': loss}

rP = pd.DataFrame(data)
print(rP)
rP.to_excel('results/recv.xlsx',index=False)
    
