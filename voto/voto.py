import math
import operator
from dataclasses import dataclass


@dataclass(order=True)
class Voto:
    materia: str
    punteggio: int
    data: str
    lode: bool

    def __str__(self):
        if self.lode:
            return f"In {self.materia} hai preso {self.punteggio} e lode il {self.data} "
        else:
            return f"In {self.materia} hai preso {self.punteggio} il {self.data} "

    def copy(self):
        return Voto(self.materia, self.punteggio, self.data, self.lode)
    #def __eq__(self, other):
    #    return (self.materia == other.materia and
    #            self.punteggio==other.punteggio and
    #            self.lode==other.lode)


class Libretto:
    def __init__(self, proprietario, voti=[]):
        self.proprietario = proprietario
        self.voti = voti

    def append(self,voto):
        if (self.hasConflitto(voto) is False
            and self.hasVoto(voto) is False):
                self.voti.append(voto)
        else:
            raise ValueError("Il voto è già presente")

    def __str__(self):
        mystr=f"Libretto voti di {self.proprietario} \n"
        for v in self.voti:
            mystr+= f"{v} \n"
        return mystr
    def __len__(self):
        return len(self.voti)

    def calcolaMedia(self):

        """
        restituisce la media dei voti attualmente presenti nel libretto
        :return: valore numerico della media oopure ValueError in caso la lista fosse vuota
        """

        '''
        
        v=[]
        for v1 in self.voti:
            v.append(v1.punteggio)
        '''
        #il codice sopra si può scrivere in questo modo
        if len(self.voti) == 0:
            raise ValueError("Attenzione, lista esami vuota")

        v=[v1.punteggio for v1 in self.voti]
        return sum(v)/len(v)
        #return math.mean(v)

    def getVotiByPunti(self, punti, lode):
        """
        restituisce una lista di esami con punteggio uguale a punti e lode
        :param punti: variabile di tipo intero che rappresenta il punteggio
        :param lode: variabile di tipo booleana che indica se presente la lode
        :return: restituisce una lista di voti
        """
        votiFiltrati=[]
        for v in self.voti:
            if v.punteggio == punti and v.lode == lode:
                votiFiltrati.append(v)

        return votiFiltrati

    def getVotoByName(self, nome):
        """
        restituisce un oggetto Voto della materia che corrisponde al nome passato come parametro
        :param nome: nome della materia di cui vogliamo il voto
        :return: restituisce oggetto di tipo Voto, oppure None in caso di nome non presente(voto non trovato)
        """
        for v in self.voti:
            if v.materia == nome:
                return v

    def hasVoto(self,voto):
        """
        Questo metodo verifica se il libretto contiene già il voto.
        Due voti sono considerati uguali se hanno stesso campo materia e stesso campo punteggio
        (voto è formato da due campi: punteggio e lode)
        :param voto: istanza dell'oggetto di tipo Voto
        :return: True se voto già presente, False altrimenti
        """

        for v in self.voti:
            if v.materia==voto.materia and v.punteggio==voto.punteggio and v.lode==voto.lode:
                return True

        return False

    def hasConflitto(self,voto):
        """
        Questo metodo controlla che il voto"voto" non rappresenti un conflitto con i voti già presenti
        nel Libretto. Consideriamo due voti in conflitto quando hanno lo stesso campo materia
        madiversa coppia(punteggio, lode)
        :param voto: istanza della classe Voto
        :return: True se voto è in conflitto, False altrimenti
        """

        for v in self.voti:
            if v.materia==voto.materia and not(
                v.punteggio==voto.punteggio
                and v.lode==voto.lode):
                return True

        return False


    def copy(self):
        """
        crea una nuova copia del libretto
        :return: istanza della classe Libretto
        """
        nuovo=Libretto(self.proprietario.copy(), [])
        for v in self.voti:
            nuovo.append(v.copy())
        return nuovo


    def creaMigliorato(self):
        """
        Crea un nuovo oggetto Libretto, in cui i voti sono migliorati secondo la seguente logica:
        se il voto è >= 18 e <24 aggiungo +1
        se il voto è >=24 e <29 aggiungo +2
        se il voto è 29 aggiungo +1
        se il voto è 30 rimane 30
        :return: nuovo libretto
        """

        nuovo=self.copy()


        for v in nuovo.voti:
            if 18<=v.punteggio <24:
                v.punteggio+=1
            elif 24<=v.punteggio<29:
                v.punteggio += 2
            elif v.punteggio==29:
                v.punteggio = 30
        return nuovo

    def sortByMateria(self):
        #self.voti.sort(key=estraiMateria)
        self.voti.sort(key=operator.attrgetter("materia"))


    #opzione 1: creo due metodi di stampa che prima ordinano e poi stampano
    #opzione 2: creo due metodi che ordinano la lista di self e poi un unico metodo di stampa
    #opzione 3: creo due metodi che si fanno una copia(deep) autonoma della lista, la ordinano e la restituiscono
        #poi un altro metodo si occuperà di stampare le nuove liste
    #opzione 4: creo una shallow copy(copio la lista ma gli oggetti dentro rimangono quelli vecchi)
        # di self.voti e ordino quella


    #OPZIONE 3

    def creaLibOrdinatoPerMateria(self):
        """
        Crea un nuovo oggetto Libretto, e lo ordina per materia
        :return: nuova istanza della classe Libretto
        """

        nuovo=self.copy()
        nuovo.sortByMateria()
        return nuovo

    def creaLibroOrdinatoPerVoto(self):
        """
        Crea un nuovo oggetto Libretto, e lo ordina per voto
        :return: nuova istanza della classe Libretto
        """
        nuovo=self.copy()
        nuovo.voti.sort(key=lambda v:(v.punteggio,v.lode),reverse=True)
        return nuovo

    def cancellaInferiori(self,punteggio):
        """
        Questo metodo agisce sul libretto corrente eliminando tutti i voti inferiori al parametro punteggio
        :param punteggio: intero indicante il valore minimo accettato
        :return:
        """

        #Modo 1
        #for i in range(len(self.voti)):
        #    if self.voti[i].punteggio<punteggio:
        #        self.voti.pop(i) #tolgo elementi da una lista che sto ciclando ERRORE

        #Modo 2
        #for v in self.voti:
        #    if v.punteggio<punteggio:
        #        self.voti.remove(v) stesso problema del modo1

        #Modo 3
        nuovo=[]
        for v in self.voti:
            if v.punteggio>=punteggio:
                nuovo.append(v)

        self.voti=nuovo

        #Modo 4
        #return [v for v in self.voti if v.punteggio>=punteggio]

def estraiMateria(voto):
    """
    Questo metodo restituisce il campo materia dell'oggetto voto
    :param voto: istanza della classe Voto
    :return: stringa rappresentante il nome della materia
    """

    return voto.materia

def testVoto():
    print("Ho usato voto in maniera standalone")
    v1 = Voto("Trasfigurazione", 24, "2022-02-13", False)
    v2 = Voto("Pozioni", 30, "2022-02-17", True)
    v3 = Voto("Difesa contro le arti oscure", 24, "2022-02-11", False)
    print(v1)

    mylib = Libretto(None, [v1, v2])
    print(mylib)
    mylib.append(v3)
    print(mylib)
    
if __name__ == "__main__":

    testVoto()