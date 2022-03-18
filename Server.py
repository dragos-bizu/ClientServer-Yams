import socket
import random

class Server:
    def __init__(self, host = '127.0.0.1', port = 10000): #constructorul clasei ServerTCP
        self.host = host #variabila pentru host
        self.port = port #variabila pentru port
        self.listaZ = [] #Lista pentru zaruri
        self.arr = [] #Lista unde se salveaza zarurile pastrate cu comanda KEEP
        self.R = 3 #Numarul de aruncari posibile
        #Variabile pentru fiecare linie din tabel
        self.N1 = self.N2 = self.N3 = self.N4 = self.N5 = self.N6 = self.Bonus = self.Joker = self.Tripla = self.Chinta = self.Full = self.Careu = self.Yams = self.Total = 0
        self.tabeldict = { #dictionarul unde se completeaza tabelul
            'N1' : '',
            'N2' : '',
            'N3' : '',
            'N4' : '',
            'N5' : '',
            'N6' : '',
            'BONUS' : '',
            'JOKER' : '',
            'TRIPLA' : '',
            'CHINTA' : '',
            'FULL' : '',
            'CAREU' : '',
            'YAMS' : '',
            'TOTAL' : ''
            }


    def start(self): #metoda start care porneste serverul
        # apelam constructorul clasei socket din libraria socket si ca parametrii avem AF_INET pentru a specifica tipul de adresa, in cazul nostru IPV4
        # si SOCK_STREAM pentru ca folosim TCP la nivel transport
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((self.host, self.port)) #metoda bind asociaza serverul cu adresa si portul specificat
        serverSocket.listen(2) #pregatim serverul pentru urmatoarele cereri ale clinetului
        print('Serverul asculta pe adresa: ', serverSocket.getsockname()) #Mesaj care confirma ca serverul este pornit si asculta pe o anumita adresa

        while True: #Ciclare care merge la infinit pentru a acceptat cererile clientilor
            connectionSocket, clientAddress = serverSocket.accept() #serverul accepta conexiunea
            print('Accesat de catre: ', clientAddress) #mesaj care ne confirma conexiunea creata si specifica adresa clientului
            self.__init__() #apelam constructorul clasei ServerTCP pentru a initializa variabilele jocului

            while True: #Inca o instructiune de ciclare care merge la infinit sau pana este specificat de catre client oprirea conexiunii
                messageFromClient = connectionSocket.recv(1024) #Receptionam mesajul clientului care nu trebuie sa depaseasca 1024 biti
                if messageFromClient.decode() == 'ABANDON': #Verificam daca mesajul clientului este ABANDON, iar daca este inchidem conexiunea
                    connectionSocket.close() #Cu metoda close inchidem conexiunea
                    break #iesim din a doua ciclare si ne intoarcem in prima ciclare unde asteptam o noua conexiune
                elif messageFromClient.decode() == 'REZULTAT': #Verificam daca mesajul clientului este REZULTAT, daca este ii trimitem tabelul cu rezultatul si inchidem conexiunea
                    connectionSocket.send(self.rez().encode()) #folosind metoda send trimitem clientului rezultatul cerut
                    connectionSocket.close()
                    break
                else: #daca mesajul clientului nu este unul din cele 2 de mai sus, pregatim raspunsul clientului
                    #pregatire raspuns
                    responseToClient = self.prepareResponse(messageFromClient.decode())

                    #trimitere raspuns
                    connectionSocket.send(responseToClient.encode())

    def prepareResponse(self, data): #Functia unde verificam ce mesaj are clientul pentru jocul de YAMS si returnam un mesaj in functia de cererea clientului
        if data == 'START':
            return self.tabel()
        elif data == 'ARUNCA':
            return self.arunca()
        elif data == 'N1':
            self.calc_N1()
            return self.tabel()
        elif data == 'N2':
            self.calc_N2()
            return self.tabel()
        elif data == 'N3':
            self.calc_N3()
            return self.tabel()
        elif data == 'N4':
            self.calc_N4()
            return self.tabel()
        elif data == 'N5':
            self.calc_N5()
            return self.tabel()
        elif data == 'N6':
            self.calc_N6()
            return self.tabel()
        elif data == 'PUNCTAJ':
            return self.tabel()
        elif data[0] == 'K':
            return self.keep(data)
        elif data == 'JOKER':
            self.calc_joker()
            return self.tabel()
        elif data == 'TRIPLA':
            self.calc_tripla()
            return self.tabel()
        elif data == 'CHINTA':
            self.calc_chinta()
            return self.tabel()
        elif data == 'FULL':
            self.calc_full()
            return self.tabel()
        elif data == 'CAREU':
            self.calc_careu()
            return self.tabel()
        elif data == 'YAMS':
            self.calc_yams()
            return self.tabel()
        elif data == 'PUNCTAJ':
            return self.tabel()
        else:
            return 'Comanda Eronata!'


    def tabel(self): #Metoda pentru a trimite tabelul clientului, ne folosim de dictionar
        return 'N1 -----> ' + self.tabeldict['N1'] + '\nN2 -----> ' + self.tabeldict['N2'] + '\nN3 -----> ' + self.tabeldict['N3'] + '\nN4 -----> ' + self.tabeldict['N4'] + '\nN5 -----> ' + self.tabeldict['N5'] + '\nN6 -----> ' + self.tabeldict['N6'] + '\nBONUS --> ' + self.tabeldict['BONUS'] + '\nJOKER --> ' + self.tabeldict['JOKER'] + '\nTRIPLA -> ' + self.tabeldict['TRIPLA'] + '\nCHINTA -> ' + self.tabeldict['CHINTA'] + '\nFULL ---> ' + self.tabeldict['FULL'] + '\nCAREU --> ' + self.tabeldict['CAREU'] + '\nYAMS ---> ' + self.tabeldict['YAMS'] + '\nTOTAL --> ' + self.tabeldict['TOTAL']

    def arunca(self): #Metoda care genereaza zarurile
        if self.R != 0: #Verificam daca mai sunt aruncari disponibile
            self.listaZ = [random.randint(1, 6) for i in range(5)] #Stocam valorile in lista
            self.listaZ.sort() #Sortam valorile pentru a aparea in ordine crescatoare
            self.R -= 1 #Scadem numarul de aruncari disponibile
            return str(self.listaZ) + ' R = ' + str(self.R)  #returnam lista cu zaruri si numarul aruncarile disponibile

        else:
            return 'Nu mai sunt aruncari disponibile!'
    def calc_N1(self): #Metoda pentru a calcula in tabel linia N1
        if self.tabeldict['N1'] == '': #Verificam daca a fost calculata deja
            for i in self.listaZ:
                if i == 1:
                    self.N1 += 1
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N1'] = str(self.N1)
            self.R = 2
            self.arr = []

    def calc_N2(self): #Metoda pentru a calcula in tabel linia N2
        if self.tabeldict['N2'] == '':
            for i in self.listaZ:
                if i == 2:
                    self.N2 += 2
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N2'] = str(self.N2)
            self.R = 2
            self.arr = []

    def calc_N3(self): #Metoda pentru a calcula in tabel linia N3
        if self.tabeldict['N3'] == '':
            for i in self.listaZ:
                if i == 3:
                    self.N3 += 3
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N3'] = str(self.N3)
            self.R = 2
            self.arr = []

    def calc_N4(self): #Metoda pentru a calcula in tabel linia N4
        if self.tabeldict['N4'] == '':
            for i in self.listaZ:
                if i == 4:
                    self.N4 += 4
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N4'] = str(self.N4)
            self.R = 2
            self.arr = []

    def calc_N5(self): #Metoda pentru a calcula in tabel linia N5
        if self.tabeldict['N5'] == '':
            for i in self.listaZ:
                if i == 5:
                    self.N5 += 5
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N5'] = str(self.N5)
            self.R = 2
            self.arr = []

    def calc_N6(self): #Metoda pentru a calcula in tabel linia N6
        if self.tabeldict['N6'] == '':
            for i in self.listaZ:
                if i == 6:
                    self.N6 += 6
            self.calc_total()
            self.calc_bonus()
            self.tabeldict['N6'] = str(self.N6)
            self.R = 2
            self.arr = []

    def keep(self, data): #Metoda pentru a pastra anumite zaruri
        if self.R != 0: #verificam daca exista aruncari disponibile
            a, b = data.split() #despartim mesajul clientului in 2, o parte este KEEP, iar cealalta zarurile care vor fi pastrate
            t = [int(x) for x in b.split(',')] #despartim numarul de zaruri care vor fi pastrate
            if t[0] == 0: #verificam daca clientul nu doreste sa mai pastreze nimic
                newL = [random.randint(1, 6) for i in range(5 - len(self.arr))] #generam zarurile ramase
                self.listaZ = self.arr + newL #construim noua lista de zaruri
                self.R -= 1 #Scadem numarul de aruncari
                newL.sort() #Sortam zarurile generate
                self.listaZ.sort #sortam lista cu zaruri
                return str(newL) + ' R = ' + str(self.R) #afisam noile zaruri generate

            else:
                self.arr = self.arr + t
                newL = [random.randint(1, 6) for i in range(5 - len(self.arr))]
                self.listaZ = self.arr + newL
                self.R -= 1
                newL.sort()
                return str(newL) + ' R = ' + str(self.R)

        else:
            return 'Nu mai sunt aruncari disponibile!' #daca nu mai avem aruncari disponibile specificam clientului acest lucru

    def calc_bonus(self): #Metoda pentru a calcula in tabel linia BONUS
        if (self.N1 + self.N2 + self.N3 + self.N4 + self.N5 + self.N6) > 62:
            self.Bonus = 50
            self.tabeldict['BONUS'] = str(self.Bonus)
        else:
            self.Bonus = 0
            self.tabeldict['BONUS'] = str(self.Bonus)

    def calc_joker(self): #Metoda pentru a calcula in tabel linia JOKER
        if self.tabeldict['JOKER'] == '':
            for i in self.listaZ:
                self.Joker += i
            self.tabeldict['JOKER'] = str(self.Joker)
            self.calc_total()
            self.R = 2
            self.arr = []

    def calc_tripla(self): #Metoda pentru a calcula in tabel linia TRIPLA
        if self.tabeldict['TRIPLA'] == '':
            for i in range(1, 7):
                t = 0
                for j in self.listaZ:
                    if i == j:
                        t += 1
                if t >= 3:
                    break
            if t >= 3:
                for i in self.listaZ:
                    self.Tripla += i
                self.tabeldict['TRIPLA'] = str(self.Tripla)
                self.calc_total()
                self.R = 2
                self.arr = []
            else:
                self.Tripla = 0
                self.tabeldict['TRIPLA'] = str(self.Tripla)
                self.R = 2
                self.arr = []

    def calc_chinta(self): #Metoda pentru a calcula in tabel linia CHINTA
        if self.tabeldict['CHINTA'] == '':
            f = 0
            for i in range(1, 4):
                if self.listaZ[i] == self.listaZ[i - 1] + 1:
                    f = 1
                    break
            if f == 1:
                self.Chinta = 20
                self.tabeldict['CHINTA'] = str(self.Chinta)
                self.calc_total()
                self.R = 2
                self.arr = []
            else:
                self.Chinta = 0
                self.tabeldict['CHINTA'] = str(self.Chinta)
                self.R = 2
                self.arr = []

    def calc_full(self): #Metoda pentru a calcula in tabel linia FULL
        if self.tabeldict['FULL'] == '':
            tn = 0
            for i in range(1, 7):
                t = 0
                for j in self.listaZ:
                    if i == j:
                        t += 1
                if t == 3:
                    tn = i
                    break
            if t == 3:
                for i in range(1, 7):
                    if i == tn: i += 1
                    d = 0
                    for j in self.listaZ:
                        if i == j:
                            d += 1
                    if d == 2:
                        break
            else:
                self.Full = 0
                self.tabeldict['FULL'] = str(self.Full)
                self.R = 2
                self.arr = []
            if t == 3 and d == 2:
                self.Full = 30
                self.tabeldict['FULL'] = str(self.Full)
                self.calc_total()
                self.R = 2
                self.arr = []
            else:
                self.Full = 0
                self.tabeldict['FULL'] = str(self.Full)
                self.R = 2
                self.arr = []

    def calc_careu(self): #Metoda pentru a calcula in tabel linia CAREU
        if self.tabeldict['CAREU'] == '':
            for i in range(1, 7):
                t = 0
                for j in self.listaZ:
                    if i == j:
                        t += 1
                if t >= 4:
                    break
            if t >= 4:
                self.Careu = 40
                self.tabeldict['CAREU'] = str(self.Careu)
                self.calc_total()
                self.R = 2
                self.arr = []
            else:
                self.Careu = 0
                self.tabeldict['CAREU'] = str(self.Careu)
                self.R = 2
                self.arr = []

    def calc_yams(self): #Metoda pentru a calcula in tabel linia YAMS
        if self.tabeldict['YAMS'] == '':
            for i in range(1, 7):
                t = 0
                for j in self.listaZ:
                    if i == j:
                        t += 1
                if t == 5:
                    break
            if t == 5:
                self.Yams = 50
                self.tabeldict['YAMS'] = str(self.Yams)
                self.calc_total()
                self.R = 2
                self.arr = []
            else:
                self.Yams = 0
                self.tabeldict['YAMS'] = str(self.Yams)
                self.R = 2
                self.arr = []

    def calc_total(self): #Metoda pentru a calcula totalul punctelor obtinute
        self.Total = self.N1 + self.N2 + self.N3 + self.N4 + self.N5 + self.N6 + self.Bonus + self.Joker + self.Tripla + self.Chinta + self.Full + self.Careu + self.Yams
        self.tabeldict['TOTAL'] = str(self.Total)

    def rez(self): #Metoda pentru a calcula rezultatul final
        if self.tabeldict['N1'] == '': self.calc_N1()
        if self.tabeldict['N2'] == '': self.calc_N2()
        if self.tabeldict['N3'] == '': self.calc_N3()
        if self.tabeldict['N4'] == '': self.calc_N4()
        if self.tabeldict['N5'] == '': self.calc_N5()
        if self.tabeldict['N6'] == '': self.calc_N6()
        if self.tabeldict['BONUS'] == '': self.calc_bonus()
        if self.tabeldict['JOKER'] == '': self.calc_joker()
        if self.tabeldict['TRIPLA'] == '': self.calc_tripla()
        if self.tabeldict['CHINTA'] == '': self.calc_chinta()
        if self.tabeldict['FULL'] == '': self.calc_full()
        if self.tabeldict['CAREU'] == '': self.calc_careu()
        if self.tabeldict['YAMS'] == '': self.calc_yams()
        self.calc_total()
        return self.tabel()


server = Server() #cream un obiect al clasei ServerTCP

server.start() #pornim serverul cu ajutorul metodei start