# Prima parte dove viene inserita la lista degli utenti (delle macchine virtuali/fisiche) 
# tra cui viene effettuato lo scambio di dati (tutti connessi con ssh)

def addUser(group): 
    while True:
        nome = input('Set the name of the host: ')
        ip = input('Set the ip address of the host: ')
        porta = input('Set the port number of the host: ')
        passwd = input('Enter the password of the host: ')
        group = group + nome + '@' + ip + ' -p ' + porta + '&' + passwd +'\n'
        if input('More hosts? y/n: ') == 'n':
            break
    return group


name = ''

answer = input('Create a host file (1) or use an existing one (2): ')
if answer == '1':
    group = 'host_file\n'
    group = addUser(group)
    name = input('Name the created file: ')
    name = 'data/'+name+'.txt'
    file = open(name,'w')
    file.write(group)
    file.close()
    print('File '+ name +' saved...')
else:
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

print('\nAvalaible hosts: ')
for h in users:
    print(h[:h.index('&')])

answer = input('\nDo you want to add users to this list? (y/n): ')

if(answer == 'y'):
    group = addUser(group)
    file = open(name,'w')
    file.write(group)
    file.close()
    print('File '+ name +' saved...\n')

    g = group[group.index('\n')+1:]
    users = g.split('\n')
    users = users[0:-1]

print('\nAvalaible hosts: ')
for h in users:
    print(h[:h.index('&')])

#Definizione file con all'interno i tipi di flussi

while True:
    path = input('\nInput the path of the flow file: ')
    try:
        file = open(path,'r')
        flowFile = file.read()
        file.close()
        if 'flow_file' in flowFile:
            break
        print('Can\'t find file, try again')
    except: 
        print('Can\'t find file, try again')

flowFile = flowFile[flowFile.index('\n')+1:]
flows = flowFile.split('\n')
flows = flows[0:-1]

print('\nAvalaible types of flow:')
for flow in flows:
    print(flow)

# Inserimento dei diversi flussi tra le macchine precedentemente inserite, 
# per ogni flusso viene creato un ITGSend in modalità singleFlow, che viene salvato
# sulla macchina da cui viene lanciato lo script (IP da indicare in main pc IP address).

mainIp = input('\nSet main pc IP address: ')

num = 0
dMax = 0
send = open('data/sender','w')
recv = open('data/receiver','w')

while True: 
    print('\nAvalaible hosts: ')
    i = 0
    rec = []
    for h in users:
        print(str(i)+': '+h[:h.index('&')])
        i = i+1
        rec.append(0)
    while True:
        sd = input('\nSet a new flow between hosts in the form <sender>/<receiver> (ex: 0/1): ')
        sender = int(sd[0:sd.index('/')])
        receiver = int(sd[sd.index('/')+1:])
        if sender<len(users) and receiver<len(users):
            break
        print('Error in the input...')

    S = users[sender]
    S = S[S.index('@')+1:S.index(' ')]
    R = users[receiver]
    R = R[R.index('@')+1:R.index(' ')]

    print('\nAvalaible types of flow:')
    i = 0
    for flow in flows:
        print(str(i)+ ': '+flow)
        i = i + 1
    
    while True:
        answer = int(input('\nSelect the type of flow you want to generate: '))
        if answer<len(flows):
            break
        print('Error in the input...')

    d = input('Set the duration of the generation (in ms): ')
    amount = int(input('Select the amount of ' + flows[answer] + ' flows to generate between '+S+' and '+R+': '))

    #t = input('Set whether you want the traffic to be UDP or TCP: ')
    #d = input('Set the duration of the generation (in ms): ')
    #pps = input('Set the number of packets to generate per second: ')
    #s = input('Set the size of each packet: ')
    #send.write(users[sender].replace(' ','_')+'%-T_'+t+'_-a_'+R+'_-c_'+s+'_-C_'+pps+'_-t_'+d + '_-L_'+mainIp+'_TCP_-l_results/send'+str(num)+'.log_-X_'+mainIp+'_TCP_-x_results/recv'+str(num)+'.log ')
    
    for _ in range(amount):
        send.write(users[sender].replace(' ','_') + '%-t_' + d + '_-a_' + R + '_' + flows[answer].replace(' ','_') + '_-L_'+mainIp+'_TCP_-l_results/send'+str(num)+'.log_-X_'+mainIp+'_TCP_-x_results/recv'+str(num)+'.log ')
        num = num + 1
    
    if rec[receiver] == 0:
        rec[receiver]=1
        h = users[receiver].replace(' ','_')
        recv.write(h+' ')
    
    dMax = max(int(d),dMax)
    answer = input('Other flows? y/n: ')
    if answer == 'n':
        break

send.close()
recv.close()

dMax = dMax/1000
time = open('data/time','w')
time.write(str(dMax))
time.close()
file = open('data/number','w')
file.write(str(num))
file.close()