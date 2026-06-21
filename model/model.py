import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._anno1 = None
        self._anno2 = None
        self._bestpath = None
        self._minrange = None


    def buildGraph(self, anno1, anno2):

        self._anno1 = anno1
        self._anno2 = anno2

        nodi = self.getNodi(anno1, anno2)
        self._graph.add_nodes_from(nodi)

        self._dictConstructor = {}
        for n in nodi:
            self._dictConstructor[n.constructorId] = n

        archi = self.getArchi(anno1, anno2)
        for arco in archi:
            self._graph.add_edge(arco.u, arco.v, weight=arco.peso)

        self.filldob()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getYears(self):
        return DAO.getAllYears()

    def getNodi(self, anno1, anno2):
        return DAO.getAllNodi(anno1, anno2)

    def getNodiCompleto(self):
        return self._graph.nodes()

    def getArchi(self, anno1, anno2):
        return DAO.getAllArchi(anno1, anno2, self._dictConstructor)

    def getArchiCompleto(self):
        return (self._graph.edges(data=True))

    def getConnessa(self):

        #componente connessa di un certo nodo
        #la dimensione è la lunghezza della lista della componente len(componenti)

        componenti = list(nx.connected_components(self._graph))

        return componenti

    def getConnessaNodo(self):
        nodi = self._graph.nodes()
        #componente_massima : contiene i nodi della componente più grande
        componente_massima = max(nx.connected_components(self._graph), key=len)
        lista = list(componente_massima)
        lista.sort(key=lambda x: self._graph.degree(x), reverse=True)

        return lista, len(componente_massima)

    def filldob(self):
        for nodo in self._graph.nodes():
            dob = DAO.getAnziano(self._anno1, self._anno2, nodo.constructorId)
            nodo.oldest_driver_dob = dob[0]



    def getPath(self,k):
        self._bestpath = []
        self._minrange = 100*365

        componenti = list(nx.connected_components(self._graph))

        if len(componenti) < k:
            return None, 0

        parziale = []
        self.ricorsione(parziale,k,componenti,0)

        return self._bestpath , self._minrange

    def ricorsione(self, parziale, k, componenti, indexcomponente):

        if len(parziale) == k:

            datedinascita = [c.oldest_driver_dob for c in parziale]
            differenza = (max(datedinascita) - min(datedinascita)).days

            if differenza< self._minrange :
                self._bestpath = copy.deepcopy(parziale)
                self._minrange = differenza

            return

        if indexcomponente >= len(componenti) or (len(componenti)-indexcomponente) < (k-len(parziale)):
            return

        componente = componenti[indexcomponente]
        for c in componente:
            parziale.append(c)
            self.ricorsione(parziale, k, componenti, indexcomponente+1)
            parziale.pop()

        self.ricorsione(parziale, k, componenti, indexcomponente+1)