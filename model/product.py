from dataclasses import dataclass
@dataclass
class Product:
    id: int
    product_name: str
    quantity: int

    def __eq__(self, other):
        # Controlla se 'other' è un'istanza di Product
        if not isinstance(other, Product):
            return False  # Oppure return NotImplemented
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)
    def __lt__(self, other):
        return self.quantity < other.quantity