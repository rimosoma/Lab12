import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        lista_nazioni = self._model.passa_nazioni()
        for nazione in lista_nazioni:
            self._view.ddcountry.options.append(ft.dropdown.Option(nazione))

        for anno in [2015, 2016, 2017, 2018]:
            self._view.ddyear.options.append(ft.dropdown.Option(anno))
            self._view.update_page()


    def handle_graph(self, e):
        nazione = self._view.ddcountry.value
        anno = self._view.ddyear.value
        print(anno, nazione)
        grafo = self._model.build_Graph(nazione, anno)
        nr_nodi = len(grafo.nodes())
        nr_archi = len(grafo.edges())
        self._view.txt_result.controls.append(ft.Text(f"nr nodi = {nr_nodi}  nr archi = {nr_archi}"))
        self._view.update_page()


    def handle_volume(self, e):
        lista = self._model.lista_tuple_nodo_somma()
        for element in lista:
            self._view.txt_result.controls.append(ft.Text(f"{element}"))
            self._view.update_page()



    def handle_path(self, e):
        pass
