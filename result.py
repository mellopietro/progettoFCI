import numpy as np
import pandas as pd

file = open('data/number','r')
n = int(file.read())
file.close()

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

#sA = []
rA = []
index = []
column = []
val = True
lMax = 0

for i in range(n):
    #file = open('results/send'+str(i)+'.dat')
    #send = file.read()
    #file.close()
    file = open('results/recv'+str(i)+'.dat')
    recv = file.read()
    file.close()
    #send=send[send.index('\n')+1:]
    #s = send.split('\n')
    #s = s[:-1]
    recv = recv[recv.index('-')+1:]
    sender = recv[:recv.index('-')]
    recv=recv[recv.index('-')+1:]
    receiver = recv[:recv.index(' ')]
    recv = recv[recv.index('\n')+1:]
    r = recv.split('\n')
    r = r[:-1]
    sender = users.index(sender)
    receiver = users.index(receiver)
    for j in range(len(r)):
        if val == True:
            column.append('time: '+str(j))
        #s[j] = s[j][s[j].index(' ')+1:]
        #s[j] = s[j][:s[j].index(' ')]
        r[j] = r[j][r[j].index(' ')+1:]
        r[j] = r[j][:r[j].index(' ')]
    val = False
    #sA.append(s)
    rA.append(r)
    index.append(str(sender)+'-'+str(receiver))
    lMax = max(lMax,len(r))

#sM = np.zeros((n,len(sA[0])),dtype='float')
rM = np.zeros((n,lMax),dtype='float')


for i in range(n):
    for j in range(len(rA[i])):
        #sM[i,j] = sA[i][j]
        rM[i,j] = rA[i][j]
    
#sP = pd.DataFrame(data=sM, index=index, columns=column)
rP = pd.DataFrame(data=rM, index=index, columns=column)

#print(sM)
print(rM)
