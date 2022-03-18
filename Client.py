import socket

host = '127.0.0.1' #variabila pentru a retine hostul
port = 10000 #variabila pentru a retine portul

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #specificam ca soclul de comunicare va folosi IPV4 (AF_INET) si TCP(SOCK_STREAM)
clientSocket.connect((host, port)) #folosim metoda connect pentru a ne conecta la serverul care asculta pe adresa 127.0.0.1 (Local) si portul 10000

while True: #O ciclare care merge la infinit sau pana clientul solicita oprirea acesteia
    message = input('Introduceti Comanda: ') #Mesajul pe care clientul doreste sa il trimita

    if message == 'ABANDON': #Daca mesajul este ABANDON il trimitem serverului si iesim din ciclare
        clientSocket.send(message.encode()) #Trimitem serverului mesajul, metoda encode converteste stringul in bytes pentru a putea fi trimis
        break;
    else:
        clientSocket.send(message.encode())
        recvMessage = clientSocket.recv(2048) #Primim raspunsul serverului la cererea clientului(Maxim 2048 octeti)
        print(recvMessage.decode()) #afisam raspunsul serverului, metoda decode convertestul mesajul in string
    if message == 'REZULTAT': #Daca mesajul clientului este REZULTAT iesim din ciclare
        break;

clientSocket.close() #Incheiem conexiunea