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


print(users)

for i in range(n):
    file = open('result/send'+i+'.dat')
    send = file.read()
    file.close()
    file = open('result/recv'+i+'.dat')
    recv = file.read()
    file.close()
    send = send[send.index('-')+1:]
    sender = send[:send.index('-')]
    send=send[send.index('-')+1:]
    receiver = send[:send.index('-')]
    send=send[send.index('\n')+1:]
    s = send.split('\n')
    recv = recv[recv.index('\n')+1:]
    r = receiver.split('\n')
    sender = users.index(sender)
    receiver = users.index(receiver)
    print('i: ' + s)
    print('i: ' + r)


#matrice = np.zeros((10,10),dtype='int16')
#for i in range(10):
#    for j in range(10):
#        matrice[i,j] = i*10+j
