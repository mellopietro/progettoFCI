import numpy as np

file = open('data/number','r')
n = int(file.read())
file.close()

while True:
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

sA = []
rA = []
for i in range(n):
    file = open('results/send'+str(i)+'.dat')
    send = file.read()
    file.close()
    file = open('results/recv'+str(i)+'.dat')
    recv = file.read()
    file.close()
    send = send[send.index('-')+1:]
    sender = send[:send.index('-')]
    send=send[send.index('-')+1:]
    receiver = send[:send.index(' ')]
    send=send[send.index('\n')+1:]
    s = send.split('\n')
    s = s[:-1]
    recv = recv[recv.index('\n')+1:]
    r = recv.split('\n')
    r = r[:-1]
    sender = users.index(sender)
    receiver = users.index(receiver)
    for j in range(len(s)):
        s[j] = s[j][s[j].index(' ')+1:]
        s[j] = s[j][:s[j].index(' ')]
        r[j] = r[j][r[j].index(' ')+1:]
        r[j] = r[j][:r[j].index(' ')]
    sA.append(s)
    rA.append(r)

sM = np.zeros((n,len(sA[0])),dtype='float')
sR = np.zeros((n,len(rA[0])),dtype='float')

for i in range(n):
    for j in range(len(sA[i])):
        sM[i][j] = float(sA[i][j])
        sR[i][j] = float(rA[i][j])

print(sM)
print(sR)
