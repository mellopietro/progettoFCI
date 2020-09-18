# Prima parte dove viene inserita la lista degli utenti (delle macchine virtuali/fisiche) 
# tra cui viene effettuato lo scambio di dati (tutti connessi con ssh)

def addUser(group): 
    while True:
        nome = input('Set the username of the host: ')
        ip = input('Set the ip address of the host: ')
        porta = input('Set the port number of the host: ')
        passwd = input('Enter the password of the host: ')
        group = group + nome + '@' + ip + ' -p ' + porta + '&' + passwd +'\n'
        if input('More hosts? y/n: ') == 'n':
            break
    return group

def saveHostName(name):
    file = open('data/hosts','w')
    file.write(name)
    file.close()

answer = input('Do you want to repeat the last experiment? (y/n): ')
if answer == 'n':
    
    name = ''

    answer = input('Create a host file (1) or use an existing one (2): ')
    if answer == '1':
        group = 'host_file\n'
        group = addUser(group)
        name = input('Name the created file: ')
        name = 'data/'+name+'.txt'
        saveHostName(name)
        file = open(name,'w')
        file.write(group)
        file.close()
        print('File '+ name +' saved...')
    else:
        while True:
            name = input('Input the path of the host file: ')
            try:
                file = open('data/' + name,'r')
                group = file.read()
                file.close()
                if('host_file' in group):
                    break
                print('Can\'t find file, try again')
            except:
                print('Can\'t find file, try again')
        saveHostName('data/' + name)
    g = group[group.index('\n')+1:]
    users = g.split('\n')
    users = users[0:-1]

    print('\nAvalaible hosts: ')
    for h in users:
        print(h[:h.index('&')])

    answer = input('\nDo you want to add users to this list? (y/n): ')

    if(answer == 'y'):
        group = addUser(group)
        file = open('data/' + name,'w')
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
            file = open('data/' + path,'r')
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

    dMax = 0
    tot = []
    sen = []
    rec = []
    s = []

    for i in range(len(users)):
        sen.append(open('data/sender'+str(i),'w'))
        log = open('data/logInfo'+str(i),'w')
        log.write(users[i] + '%')
        log.write('-X '+mainIp+' TCP -x results/recv'+str(i)+'.log') #_-L_'+mainIp+'_TCP_-l_results/send'+str(num)+'.log
        log.close()
        rec.append(0)
        s.append(0)
        tot.append(0)

    while True: 
        answer = input('\nDo you want to use a predefined file? (y/n): ')
        if answer == 'n':
            print('\nAvalaible hosts: ')
            for i in range(len(users)):
                print(str(i)+': '+users[i][:users[i].index('&')])

            while True:
                try:
                    sd = input('\nSet a new flow between hosts in the form <sender>/<receiver> (ex: 0/1): ')
                    sender = int(sd[0:sd.index('/')])
                    receiver = int(sd[sd.index('/')+1:])
                    if sender<len(users) and receiver<len(users):
                        break
                    print('Error in the input...')
                except:
                    print('Error in the input...')

            S = users[sender]
            S = S[S.index('@')+1:S.index(' ')]
            R = users[receiver]
            R = R[R.index('@')+1:R.index(' ')]

            print('\nAvalaible types of flow:')
            for i in range(len(flows)):
                print(str(i) + ': ' + flows[i])

            while True:
                try:
                    answer = int(input('\nSelect the type of flow you want to generate: '))
                    if answer<len(flows):
                        break
                    print('Error in the input...')
                except:
                    print('Error in the input...')


            d = int(input('Set the duration of the generation (in ms): '))
            amount = int(input('Select the amount of ' + flows[answer] + ' to generate between '+S+' and '+R+': '))

            for _ in range(amount):
                sen[sender].write('-m rttm -t ' + str(d) + ' -a ' + R + ' ' + flows[answer] + '\n')
                tot[sender] = tot[sender] + 1

            rec[receiver] = 1
            s[sender] = 1


            dMax = max(int(d),dMax)

        else:
            while True:
                try:
                    name = input('Input the name of the file: ')
                    file = open(name,'r')
                    config = file.read()
                    file.close()
                    if 'config_file' in config:
                        break
                    print('Can\'t find file, try again')
                except: 
                    print('Can\'t find file, try again')


            for _ in range(config.count('\n')):
                config = config[config.index('\n')+1:]
                sender = int(config[0:config.index('/')])
                receiver = int(config[config.index('/')+1:config.index(' ')])
                config = config[config.index(' ')+1:]
                opt = int(config[0:config.index(' ')])
                config = config[config.index(' ')+1:]
                d = int(config[0:config.index(' ')])
                config = config[config.index(' ')+1:]
                amount = int(config[0:config.index(';')])

                try: 
                    R = users[receiver]
                    R = R[R.index('@')+1:R.index(' ')]
                    for _ in range(amount):
                        sen[sender].write('-m rttm -t ' + str(d) + ' -a ' + R + ' ' + flows[opt] + '\n')
                        tot[sender] = tot[sender] + 1
                    rec[receiver] = 1
                    s[sender] = 1
                    dMax = max(d,dMax)
                except:
                    print('Error in the input file...')


        answ = input('Other flows? y/n: ')
        if answ == 'n':
            break



    on = open('data/on','w')
    recv = open('data/receiver','w')
    for i in range(len(users)):
        if rec[i] == 1:
            recv.write(users[i] + '%')
        if s[i] == 1:
            on.write(str(i) + ' ')
        sen[i].close()
    on.close()
    recv.close()

    dMax = dMax/1000
    dMax = dMax + max(tot)
    time = open('data/time','w')
    time.write(str(dMax))
    time.close()