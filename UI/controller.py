from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._view.txt_risultato.clean()
        self._view.dd_prodotto_iniziale.clean()
        self._view.dd_prodotto_finale.clean()
        start_date, end_date = self._view.dp1.value, self._view.dp2.value
        category = self._view.dd_category.value
        graph = self._model.create_graph(start_date,end_date,category)
        self._view.txt_risultato.controls.append(ft.Text(f'Date selezionate:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Start date: {start_date.date()}'))
        self._view.txt_risultato.controls.append(ft.Text(f'End date: {end_date.date()}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Grafo correttamente creato:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Numero di nodi: {graph.number_of_nodes()}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Numero di archi: {graph.number_of_edges()}\n'))
        self.load_dd_prodotto(graph)
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        self._view.txt_risultato.controls.append(ft.Text(f'I cinque prodotti più venduti sono:'))
        top_five = self._model.get_top_five()
        for top in top_five:
            self._view.txt_risultato.controls.append(ft.Text(f'{top[0].product_name} with score {top[1]}'))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        self._view.txt_risultato.clean()
        start = self._view.dd_prodotto_iniziale.value
        end = self._view.dd_prodotto_finale.value
        l_max = self._view.txt_lunghezza_cammino.value
        path, peso = self._model.get_info(start, end, int(l_max))
        self._view.txt_risultato.controls.append(ft.Text(f'Cammino migliore:'))
        for p in path:
            self._view.txt_risultato.controls.append(ft.Text(f'{p.product_name}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Score: {peso}'))
        self._view.update()

    def load_dd_categories(self):
        """ Load dd category """
        categories = self._model.get_categories()
        options_categories = []
        for category in categories:
            options_categories.append(ft.DropdownOption(key=category['id'], text=category['category_name']))
        return options_categories

    def load_dd_prodotto(self,graph):
        nodes = graph.nodes()
        for n in nodes:
            self._view.dd_prodotto_iniziale.options.append(ft.DropdownOption(key=n.id, text=n.product_name))
            self._view.dd_prodotto_finale.options.append(ft.DropdownOption(key=n.id, text=n.product_name))

