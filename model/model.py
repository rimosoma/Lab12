from typing import Any, List

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

    def heaviest_path(self, lunghezza):
        """
        Metodo di ingresso: inizializza lo stato e chiama la ricorsione.
        Restituisce il percorso più lungo (#archi) di archi
        """
        self._best_path = []
        self.peso_best = float('-inf')  # Inizializza con un valore molto basso

        # Itera su tutti i nodi nel grafo e avvia una DFS da ognuno
        for start_node_id in self.iMap.keys():  # self.iMap.keys() dovrebbe darti gli ID dei nodi
            self._dfs(current=start_node_id, path=[start_node_id], lunghezza=lunghezza)

        # ... (il resto del codice per formattare l'output)
        res = f""
        if not self._best_path or self.peso_best == float('-inf'):
            return "Nessun percorso chiuso della lunghezza specificata trovato."

        for i in range(lunghezza):
            node1_idx = self._best_path[i]
            node2_idx = self._best_path[i + 1]
            # Assumendo self.iMap[idx] per ottenere il nome originale del nodo
            res += f"{node1_idx} -> {node2_idx} (Peso: {self.graph[node1_idx][node2_idx]['weight']}) \n"

        res += f"e il peso totale: {self.peso_best}"

        return res

    def _dfs(self, current: Any, path: List[Any], lunghezza:int):
        """
        Metodo ricorsivo:
           E: sempre eseguito
           A: caso base
           B: genera scelte
           C: filtro + ricorsione
           D: backtracking
        """
        # — E: controllo e aggiorno il best_path se questo è più lungo
        #       (numero di archi = len(path)-1)

        if len(path) == lunghezza + 1:
            if path[0] == path[lunghezza]:
                peso_archi = 0
                for i in range(lunghezza):  # Itera 'lunghezza' volte per 'lunghezza' archi
                    node1_idx = path[i]
                    node2_idx = path[i + 1]
                    peso_archi += self.graph[node1_idx][node2_idx]["weight"]

                if peso_archi > self.peso_best:
                    self._best_path = path.copy()
                    self.peso_best = peso_archi
            return


        # — B: per ogni possibile arco uscente
        for neigh in self.graph.neighbors(current):
            w = self.graph[current][neigh]["weight"]

            # — C: filtro: permetto di tornare al nodo iniziale solo se è la fine del percorso
            if neigh not in path or (len(path) == lunghezza and neigh == path[0]):
                path.append(neigh)
                self._dfs(current=neigh, path=path, lunghezza=lunghezza)
                # — D: backtracking
                path.pop()







