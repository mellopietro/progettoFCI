import numpy as np
import pandas as pd

while True:
    try: 
        file = open('data/hosts','r')
        name =file.read()
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

for i in range(len(users)):
    file = open('results/recv'+str(i)+'.dat')
    recv = file.read()
    file.close()
    n = []
    sender = []
    receiver = []
    while True:
        n.append(int(recv[recv.index(' ')+1:recv.index('-')]))
        recv = recv[recv.index('-')+1:]
        sender.append(recv[:recv.index('-')])
        recv=recv[recv.index('-')+1:]
        receiver.append(recv[:recv.index(' ')])
        recv = recv[recv.index(' '):]
        if recv[:recv.index('\n')] == ' Aggregate-Flow':
            recv = recv[recv.index('\n')+1:]
            break

    data = {'Flow': n, 'Sender': sender, 'Receiver': receiver}
 
    col = recv.count('\n')

    for _ in range(col):
        t = 'Time ' + str(float(recv[:recv.index(' ')]))
        recv = recv[recv.index(' ')+1:]
        val = []
        for _ in range(len(n)):
            val.append(float(recv[:recv.index(' ')]))
            recv = recv[recv.index(' ')+1:]
        recv = recv[recv.index('\n')+1:]
        data[t] = val

    rP = pd.DataFrame(data,index=n)
    rP = rP.sort_values(by=['Flow'])
    print(rP)
    rP.to_excel('results/recv'+str(i)+'.xlsx', index=False)
    