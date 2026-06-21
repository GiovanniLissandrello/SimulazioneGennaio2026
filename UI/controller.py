import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno1 = None
        self._anno2 = None

    def fillddAnno1(self):

        lista_anni = self._model.getYears()
        for anno in lista_anni:
            self._view._ddAnno1.options.append(
                ft.dropdown.Option(data=anno,
                                   key=anno,
                                   text=anno,
                                   on_click=self.read_anno1)
            )

    def read_anno1(self, e):
        if e.control.data is None:
            self._anno1 = None
        else:
            self._anno1 = e.control.data

    def fillddAnno2(self):

        lista_anni = self._model.getYears()
        for anno in lista_anni:
            self._view._ddAnno2.options.append(
                ft.dropdown.Option(data=anno,
                                   key=anno,
                                   text=anno,
                                   on_click=self.read_anno2)
            )

    def read_anno2(self, e):
        if e.control.data is None:
            self._anno2 = None
        else:
            self._anno2 = e.control.data

    def handleCreaGrafo(self,e):

        if self._anno1 is None or self._anno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))

        self._model.buildGraph(self._anno1, self._anno2)
        n, m = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo è costituito di {n} nodi ed {m} archi"))

        self._view.update_page()

    def handleDettagli(self, e):

        archi = self._model.getArchiCompleto()
        lista = list(archi)
        lista.sort(key=lambda x: x[2]["weight"], reverse = True)
        self._view.txt_result.controls.append(
            ft.Text(f"I 3 Archi di peso maggiore: "))

        c = 0
        for arco in lista:
            self._view.txt_result.controls.append(
                ft.Text(f"{arco[0].name} <-> {arco[1].name} ({arco[2]["weight"]})"))
            c += 1
            if c == 3:
                break

        componenti = self._model.getConnessa()
        self._view.txt_result.controls.append(
            ft.Text(f"Il numero delle componenti connese è: {len(componenti)}"))


        lista, dimensione = self._model.getConnessaNodo()
        self._view.txt_result.controls.append(
            ft.Text(f"dimensione massima: {dimensione}, con nodi : "))

        for nodo in lista:
            self._view.txt_result.controls.append(
                ft.Text(nodo))
        self._view.update_page()

    def handleCerca(self, e):

        bestPath, minRange = self._model.getPath(int(self._view._txtInK.value))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"{minRange}"))

        self._view.update_page()

