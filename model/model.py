import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.iMap = {}
        self.graph = nx.Graph()

    def passa_nazioni(self):
        return DAO.getAllNations()

    def build_Graph(self, nazione, anno):
        elenco_retailer = DAO.getRetailerNazione(nazione)
        for retailer in elenco_retailer:
            self.iMap[retailer.Retailer_code] = retailer
            self.graph.add_node(retailer.Retailer_code)


        lista_archi = DAO.getArchi(nazione, anno)
        for tripla in lista_archi:
            nodoP = tripla[0]
            nodoA = tripla[1]
            peso = tripla[2]
            self.graph.add_edge(nodoP, nodoA, weight=peso)
        return self.graph

    def lista_tuple_nodo_somma(self):
        lista_tuple = []
        nodi = self.graph.nodes()
        for nodo in nodi:
            vicini = self.graph.neighbors(nodo)
            volume = 0
            stringa = ""
            for vicino in vicini:
                volume += self.graph[nodo][vicino]["weight"]
            retailer = self.iMap[nodo]
            nome = retailer.Retailer_name
            lista_tuple.append((volume, nome))
            print(volume, nome)
        lista_tuple.sort(key=lambda x: x[0], reverse=True)
        return lista_tuple




