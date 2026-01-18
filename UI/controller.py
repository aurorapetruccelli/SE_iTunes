import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self._selected_album=None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            durata = int(self._view.txt_durata.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la durata")
            return

        self._model.crea_grafo(durata)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {self._model.G.number_of_nodes()} album, {self._model.G.number_of_edges()} archi"))


        self._view.dd_album.options.clear()
        for r in self._model.get_nodes():
            option = ft.dropdown.Option(r.title)
            self._view.dd_album.options.append(option)

        self._view.dd_album.update()
        self._view.page.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """
        titolo = e.control.value
        self._selected_album = next((id for id,oggetto in self._model.album_durata.items() if oggetto.title == titolo), None)


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if not self._selected_album:
            self._view.show_alert("Inserisci un album dal dropdown")
            return

        dimensioni, secondi = self._model.get_componente_connessa(self._selected_album)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensioni componente: {dimensioni}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Durata totale: {secondi}"))
        self._view.page.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        if not self._selected_album:
            self._view.show_alert("Inserisci un album dal dropdown")
            return

        try:
            durata = float(self._view.txt_durata_totale.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la durata")
            return

        lista_tuple,num_set,durata = self._model.ricerca(self._selected_album,durata)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato {num_set}, durata {durata} minuti"))
        for tupla in lista_tuple:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{tupla[0]} ({tupla[1]} minuti)"))
        self._view.page.update()
