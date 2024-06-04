import datetime
import json

from Product import Product


class ProductNotFoundError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class FileHandler:
    @staticmethod
    def write_to_file(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r') as f:
            return json.load(f)


class ShoppingList:
    history = []

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                return
        raise ProductNotFoundError(f"Product '{product_name}' not found in the shopping list.")

    def edit_product(self, product_name, quantity=None, price=None, notes=None):
        for product in self.products:
            if product.name == product_name:
                product.edit(quantity, price, notes)
                return
        raise ProductNotFoundError(f"Product '{product_name}' not found in the shopping list.")

    def mark_product_as_bought(self, product_name):
        for product in self.products:
            if product.name == product_name:
                product.mark_as_bought()
                self.history.append((product, datetime.datetime.now()))
                return
        raise ProductNotFoundError(f"Product '{product_name}' not found in the shopping list.")

    def display_products(self):
        for product in self.products:
            print(product)

    def filter_products(self, criterion):
        if criterion == "bought":
            return [product for product in self.products if product.bought]
        elif criterion == "not bought":
            return [product for product in self.products if not product.bought]
        elif criterion == "category":
            category = input("Enter category to filter by: ")
            return [product for product in self.products if product.category == category]
        else:
            raise ValueError(f"Unknown filter criterion: {criterion}")

    def display_history(self):
        for product, date in self.history:
            print(f"{product} bought on {date}")

    def generate_statistics(self):
        total_spent = sum(product.price * product.quantity for product in self.products if product.bought)
        average_spent = total_spent / len(self.products) if self.products else 0
        most_frequent = max(self.products, key=lambda p: p.quantity) if self.products else None
        stats = {
            "total_spent": total_spent,
            "average_spent": average_spent,
            "most_frequent_product": most_frequent
        }
        return stats

    def write_to_file(self, filename):
        data = [product.__dict__ for product in self.products]
        FileHandler.write_to_file(filename, data)

    def read_from_file(self, filename):
        data = FileHandler.read_from_file(filename)
        self.products = [Product(**item) for item in data]


# Example usage
if __name__ == "__main__":
    shopping_list = ShoppingList()
    product1 = Product(name="Milk", quantity=2, category="Dairy", price=3.5, notes="Organic")
    product2 = Product(name="Bread", quantity=1, category="Bakery", price=2.0, notes="Whole grain")
    shopping_list.add_product(product1)
    shopping_list.add_product(product2)
    shopping_list.display_products()  # Display current products

    shopping_list.mark_product_as_bought("Milk")
    shopping_list.display_history()  # Display purchase history

    print(shopping_list.filter_products("not bought"))  # Filter products not bought
    shopping_list.edit_product("Bread", price=1.5)  # Edit product details
    shopping_list.display_products()  # Display updated products

    stats = shopping_list.generate_statistics()
    print(f"Total spent: {stats['total_spent']}, Average spent: {stats['average_spent']}, Most frequent product: {stats['most_frequent_product']}")

