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
                        self.G.add_edge(p1, p2, weight=q1+q2)
                    elif q2 > q1:
                        # Arco dal maggiore al minore
                        self.G.add_edge(p2, p1, weight=q1+q2)
                    else:
                        # CASO PARITÀ (q1 == q2): Entrambi gli archi
                        self.G.add_edge(p1, p2, weight=q1+q2)
                        self.G.add_edge(p2, p1, weight=q1+q2)
        return self.G

    def get_top_five(self):
        top_five = []
        for node in self.G.nodes:
            value = 0
            out_e = self.G.out_edges(node)
            in_e = self.G.in_edges(node)
            for o in out_e:
                value += self.G[o[0]][o[1]]['weight']
            for i in in_e:
                value -= self.G[i[0]][i[1]]['weight']
            top_five.append((node, value))
        top_five.sort(key=lambda x: x[1], reverse=True)
        return top_five[:5]

    def get_max_recursive(self, current_node, parz, peso_parz, visited):
        # 1. Caso base: se ho raggiunto la lunghezza massima
        if len(parz) == self.l_max:
            # Controllo se sono arrivato alla destinazione corretta
            if current_node == self.end:
                if peso_parz > self.peso_tot:
                    self.peso_tot = peso_parz
                    self.path_max = list(parz)
            return

        # 2. Esplorazione: proseguo solo se non ho ancora raggiunto l_max
        for neighbor in self.G.successors(current_node):
            if neighbor not in visited:
                edge_weight = self.G[current_node][neighbor]['weight']

                visited.add(neighbor)
                parz.append(neighbor)

                # Ricorsione
                self.get_max_recursive(neighbor, parz, peso_parz + edge_weight, visited)

                # Backtracking
                parz.pop()
                visited.remove(neighbor)

    def get_info(self, start_id, end_id, l_max):
        start_node = self.products_dict[int(start_id)]
        self.end = self.products_dict[int(end_id)]
        self.l_max = l_max

        self.peso_tot = -float('inf')  # Inizializza a meno infinito
        self.path_max = []

        self.get_max_recursive(start_node, [start_node], 0, {start_node})

        return self.path_max, self.peso_tot


