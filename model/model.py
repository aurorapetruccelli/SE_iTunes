import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.G = nx.Graph()

        self.album = []
        self.album_playlist = []

        self.album_durata = {}


    def crea_grafo(self,durata):
        self.album = DAO.get_album_durata(durata)
        for album in self.album:
            self._nodes.append(album.id)
            self.album_durata[album.id] = album
            self.G.add_node(album.id)

        self.album_playlist = DAO.get_album_connessi()
        for coppie in self.album_playlist:
            a1 = coppie[0]
            a2 = coppie[1]
            if a1 in self._nodes and a2 in self._nodes:
                self._edges.append((a1,a2))
                self.G.add_edges_from(self._edges)

        print(self.G)

    def get_nodes(self):
        result = []
        for nodo in self.G.nodes():
            result.append(self.album_durata[nodo])

        return result


    def get_componente_connessa(self,nodo):
        componente_connessa = nx.node_connected_component(self.G,nodo)

        durata_totale = 0.0
        numero_componente_connessa = 0
        for componente in componente_connessa:
            durata_totale += float(self.album_durata[componente].duration)
            numero_componente_connessa += 1

        return numero_componente_connessa, durata_totale

    def ricerca(self,nodo,minuti_max):
        componente = nx.node_connected_component(self.G,nodo)
        self.soluzione_migliore = []
        self.ricorsione(componente,[nodo],self.album_durata[nodo].duration,minuti_max)

        dizionario = [] #dizionario con chiave nome , valore minuti
        a =0
        b = 0
        for e in self.soluzione_migliore:
            dizionario.append((self.album_durata[e].title,float(self.album_durata[e].duration)))
            a+=1
            b+=float(self.album_durata[e].duration)

        return dizionario,a,b


    def ricorsione(self,componenti,set_corrente, durata_corrente,minuti_max):
        # considero solo i nodi connessi al nodo di partenza, e volgio trovare il percorso più "lungo"
        if len(set_corrente)>len(self.soluzione_migliore):
            self.soluzione_migliore = set_corrente[:]

        for componente in componenti:
            if componente in set_corrente:
                continue
            durata = durata_corrente + self.album_durata[componente].duration
            if durata<minuti_max:
                set_corrente.append(componente)
                self.ricorsione(componenti,set_corrente,durata,minuti_max)
                set_corrente.pop()


