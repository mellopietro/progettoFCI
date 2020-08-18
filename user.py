# Prima parte dove viene inserita la lista degli utenti (delle macchine virtuali/fisiche) 
# tra cui viene effettuato lo scambio di dati (tutti connessi con ssh)

answer = input('Create a host file (1) or use an existing one (2): ')
if answer == '1':
    group = 'host_file\n'
    while True:
        nome = input('Set the name of the host: ')
        ip = input('Set the ip address of the host: ')
        porta = input('Set the port number of the host: ')
        group = group + nome + '@' + ip + ' -p ' + porta + '\n'
        if input('More hosts? y/n: ') == 'n':
            break
    name = input('Name the created file: ')
    file = open('data/'+name+'.txt','w')
    file.write(group)
    file.close()
    print('File '+ name +'.txt saved in data folder...')
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
group = group[group.index('\n')+1:]
users = group.split('\n')
users = users[0:-1]

# Inserimento dei diversi flussi tra le macchine precedentemente inserite, 
# per ogni flusso viene creato un ITGSend in modalità singleFlow, che viene salvato
# sulla macchina da cui viene lanciato lo script (IP da indicare in main pc IP address).

mainIp = input('Set main pc IP address: ')

num = 0
dMax = 0
send = open('data/sender','w')
recv = open('data/receiver','w')

while True: 
    print('Avalaible hosts: ')
    i = 0
    rec = []
    for h in users:
        print(str(i)+': '+h)
        i = i+1
        rec.append(0)

    sd = input('Set a new flow between hosts in the form <sender>/<receiver> (ex: 0/1): ')
    sender = int(sd[0:sd.index('/')])
    receiver = int(sd[sd.index('/')+1:])
    S = users[sender]
    S = S[S.index('@')+1:S.index(' ')]
    R = users[receiver]
    R = R[R.index('@')+1:R.index(' ')]
    print('Details of the flow between '+S+' and '+R+': ')
    t = input('Set whether you want the traffic to be UDP or TCP: ')
    d = input('Set the duration of the generation (in ms): ')
    pps = input('Set the number of packets to generate per second: ')
    s = input('Set the size of each packet: ')
    send.write(users[sender].replace(' ','_')+'%-T_'+t+'_-a_'+R+'_-c_'+s+'_-C_'+pps+'_-t_'+d + '_-L_'+mainIp+'_TCP_-l_results/send'+str(num)+'.log_-X_'+mainIp+'_TCP_-x_results/recv'+str(num)+'.log ')
    if rec[receiver] == 0:
        rec[receiver]=1
        h = users[receiver].replace(' ','_')
        recv.write(h+' ')
    dMax = max(int(d),dMax)
    num = num + 1
    answer = input('Other flows? y/n: ')
    if answer == 'n':
        break

send.close()
recv.close()

dMax = dMax/1000
time = open('data/time','w')
time.write(str(dMax))
time.close()