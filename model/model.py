from database.impianto_DAO import ImpiantoDAO
from model.impianto_DTO import Impianto
from datetime import datetime
'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        consumi_mese_imp1 = []
        consumi_mese_imp2= []
        for consumo in self._consumi:
            if mese == int(consumo.data.month) and consumo.id_impianto == 1:
                consumi_mese_imp1.append(consumo.kwh)
            elif mese ==int(consumo.data.month) and consumo.id_impianto == 2:
                consumi_mese_imp2.append(consumo.kwh)
        count1=0
        for kwh in consumi_mese_imp1:
            count1 += 1
        somma1=0
        for kwh in consumi_mese_imp1:
            somma1 += kwh
        media1= somma1/count1
        somma2 = 0
        count2 = 0
        for kwh in consumi_mese_imp1:
            count2 += 1
        for kwh in consumi_mese_imp2:
            somma2 += kwh
        media2 = somma2/count2
        lista_tuple=[]
        lista_tuple.append((1, media1))
        lista_tuple.append((2, media2))
        #print(lista_tuple)             #debug
        return lista_tuple

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto , costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """   #se giorno = 8, significa che ho 7 consumi in parziale, dunque avvio confronto
        if len(sequenza_parziale) == 7:         #perche 8? perche dopo considera consumo in pos 8-1=7
            #print(sequenza_parziale[:])            #DEBUG
            #print(costo_corrente)  # debug
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente            #salvo se sto consumo è migliore, (1'giro mi salva a ct ott=0)
                self.__sequenza_ottima = sequenza_parziale[:]
                print(self.__sequenza_ottima)
                print(self.__costo_ottimo)
                return
        else:                                       #imp = chiave del dizionario, dunque è per ciclare le chiavi
            for imp in consumi_settimana.keys():        #le chiavi sono solo : '1' e '2' i values le liste di consumi per ciascun imp
                k_ct=0     #aggiungo 5eur per ogni cambio dunque pongo il coefficiente, che setto eventualemente in pos dopo nella ricorsione
                kwh = consumi_settimana[imp][giorno -1]     #accedo in pos (giorno-1) perche al primo giro il consumo è in pos 0
                sequenza_parziale.append(imp)
                if len(sequenza_parziale) !=1 and len(sequenza_parziale) !=0:#ho piu 2 elementi dunque confronto=> addebito costo additivo o meno
                    if sequenza_parziale[-1] != sequenza_parziale[-2]:  #se non coincidono gli impianti dunque addebito
                        k_ct =1
                self.__ricorsione(sequenza_parziale, giorno +1, imp , costo_corrente +kwh +5*k_ct, consumi_settimana)
                sequenza_parziale.pop()     #backtrack

    def get_consumi(self):
        self._consumi = []  # Lista vuota
        for impianto in self._impianti:
            self._consumi.extend(impianto.get_consumi())        #aggiunge elemento per elemento della lista alla lista esterna
        return self._consumi

    def get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, .., kwh_giorno7]}
        """
        risultato={}
        for consumo in self._consumi:
            if mese ==  int(consumo.data.month):
                if consumo.data.day <= 7:
                    risultato.setdefault(consumo.id_impianto, []).append(consumo.kwh)
        #print(risultato)               #debug
        return risultato

