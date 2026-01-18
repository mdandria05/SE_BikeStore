from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.products_dict = {}

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        categories_list = DAO.get_category()
        return categories_list

    def get_products(self,start_date, end_date, category):
        products_list = DAO.get_products(start_date, end_date, category)
        for product in products_list:
            self.products_dict[product.id] = product

    def create_graph(self,start_date, end_date, category):
        self.G.clear()
        self.get_products(start_date, end_date, category)
        lista_prodotti = list(self.products_dict.values())

        self.G.add_nodes_from(lista_prodotti)

        for i in range(len(lista_prodotti)):
            for j in range(i + 1, len(lista_prodotti)):
                p1 = lista_prodotti[i]
                p2 = lista_prodotti[j]

                # TRASFORMAZIONE NONE -> 0
                # Usiamo l'operatore 'or 0' che è molto compatto:
                # se p1.quantity è None (o 0), q1 diventa 0.
                q1 = p1.quantity if p1.quantity is not None else 0
                q2 = p2.quantity if p2.quantity is not None else 0

                # CONDIZIONE: Entrambi devono essere stati venduti (q > 0)
                if q1 > 0 and q2 > 0:
                    if q1 > q2:
                        # Arco dal maggiore al minore
                        self.G.add_edge(p1, p2, weight=q1)
                    elif q2 > q1:
                        # Arco dal maggiore al minore
                        self.G.add_edge(p2, p1, weight=q2)
                    else:
                        # CASO PARITÀ (q1 == q2): Entrambi gli archi
                        # Qui è dove spesso si perdono gli archi "mancanti"
                        self.G.add_edge(p1, p2, weight=q1)
                        self.G.add_edge(p2, p1, weight=q2)

        print(f"Nodi: {self.G.number_of_nodes()}, Archi: {self.G.number_of_edges()}")
        return self.G



