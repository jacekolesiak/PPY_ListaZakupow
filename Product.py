class Product:
    def __init__(self, name, quantity, category, price, notes="", bought=False):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.price = price
        self.notes = notes
        self.bought = bought

    def __str__(self):
        return (f"Product(name='{self.name}', quantity={self.quantity}, category='{self.category}', "
                f"price={self.price}, notes='{self.notes}', bought={self.bought})")

    def mark_as_bought(self):
        self.bought = True

    def edit(self, quantity=None, price=None, notes=None):
        if quantity is not None:
            self.quantity = quantity
        if price is not None:
            self.price = price
        if notes is not None:
            self.notes = notes

# Example usage
if __name__ == "__main__":
    p = Product(name="Milk", quantity=2, category="Dairy", price=3.5, notes="Organic")
    print(p)  # Output: Product(name='Milk', quantity=2, category='Dairy', price=3.5, notes='Organic', bought=False)
    p.mark_as_bought()
    print(p)  # Output: Product(name='Milk', quantity=2, category='Dairy', price=3.5, notes='Organic', bought=True)
    p.edit(quantity=3, price=3.0, notes="On sale")
    print(p)  # Output: Product(name='Milk', quantity=3, category='Dairy', price=3.0, notes='On sale', bought=True)
