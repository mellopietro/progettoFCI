# progettoFCI

Progetto estivo di FCI. 

Utilizzo libreria D-ITG per creare script che permetta di automatizzare la creazione di traffico su una rete.

Operazioni preliminari necessarie per utilizzare il software:
    Installare su tutte le macchine usate i programmi screen e d-itg

        ubuntu-based distro: sudo apt install d-itg screen
        
Per lanciare il programma:

    Andare sulla cartella scaricata (progettoFCI)
        cd <path>/progettoFCI

    Dare il permesso di scrittura a script.sh
        chmod +x script.sh

    Eseguire lo script
        ./script.sh


Per salvare i risultati su file excel:

    Andare sulla cartella scaricata (progettoFCI)
        cd <path>/progettoFCI

    Dare il permesso di scrittura a script.sh
        chmod +x computation.sh

    Eseguire lo script
        ./computation.sh


Possono essere aggiunti sul programma dei flussi customizzati:

    Andare sul file data/flows.txt
        nano data/flows.txt

    Aggiungere le linee desiderate (senza eliminare la prima linea con scritto flow_file)

Possono essere aggiunti sul programma dei gruppi di flussi customizzati:

    Andare sul file data/config.txt
        nano data/config.txt

    Aggiungere le linee desiderate (senza eliminare la prima linea con scritto config_file)
    sintassi: 
        "<sender>/<receiver> <numero di flusso (vedi lanciando script.sh)> <durata flusso in millisecondi> <numero di flussi uguali>"