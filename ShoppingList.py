import datetime
import json

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
    def __init__(self):
        self.products = []
        self.history = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                return
        raise ProductNotFoundError(f"Product '{product_name}' not found in the shopping list.")

    def edit_product(self, product_name, quantity=None, price=None, notes=None, category=None):
        for product in self.products:
            if product.name == product_name:
                product.edit(quantity, price, notes, category)
                return
        raise ProductNotFoundError(f"Product '{product_name}' not found in the shopping list.")

    def mark_product_as_bought(self, product_name):
        for product in self.products:
            if product.name == product_name:
                product.mark_as_bought()
                product_for_history = Product(product.name, product.quantity, product.category, product.price,
                                              product.notes, True)
                self.history.append((product_for_history, datetime.datetime.now()))
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
        elif criterion == "price range":
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
            return [product for product in self.products if min_price <= product.price <= max_price]
        elif criterion == "quantity":
            min_quantity = int(input("Enter minimum quantity: "))
            max_quantity = int(input("Enter maximum quantity: "))
            return [product for product in self.products if min_quantity <= product.quantity <= max_quantity]
        elif criterion == "notes":
            keyword = input("Enter keyword to search in notes: ").lower()
            return [product for product in self.products if keyword in product.notes.lower()]
        else:
            raise ValueError(f"Unknown filter criterion: {criterion}")

    def display_history(self):
        for product, date in self.history:
            print(f"{product} bought on {date}")

    def generate_statistics(self):
        total_spent = sum(product.price * product.quantity for product in self.products if product.bought)
        average_spent = total_spent / len(self.products) if self.products else 0

        product_counts = {}
        for product, _ in self.history:
            if product.name in product_counts:
                product_counts[product.name] += 1
            else:
                product_counts[product.name] = 1

        most_frequent_product = max(product_counts, key=product_counts.get) if product_counts else None

        stats = {
            "total_spent": total_spent,
            "average_spent": average_spent,
            "most_frequent_product": most_frequent_product
        }
        return stats

    def write_to_file(self, filename):
        data = [product.__dict__ for product in self.products]
        FileHandler.write_to_file(filename, data)

    def read_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.products = [Product(**item) for item in data]
        except FileNotFoundError:
            print(f"File '{filename}' not found. Creating an empty shopping list.")
            self.products = []

    def save_history_to_file(self, filename):
        data = [(product.__dict__, str(date)) for product, date in self.history]
        FileHandler.write_to_file(filename, data)

    def load_history_from_file(self, filename):
        try:
            data = FileHandler.read_from_file(filename)
            if data:
                self.history = [(Product(**item[0]), datetime.datetime.fromisoformat(item[1])) for item in data]
            else:
                print(f"File '{filename}' is empty. Initializing an empty purchase history.")
                self.history = []
        except FileNotFoundError:
            print(f"File '{filename}' not found. Initializing an empty purchase history.")
            self.history = []

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

    def __repr__(self):
        return self.__str__()

    def mark_as_bought(self):
        self.bought = True

    def edit(self, quantity=None, price=None, notes=None, category=None):
        if quantity is not None:
            self.quantity = quantity
        if price is not None:
            self.price = price
        if notes is not None:
            self.notes = notes
        if category is not None:
            self.category = category


def main():
    shopping_list = ShoppingList()
    shopping_list.read_from_file("shopping_list.json")
    shopping_list.load_history_from_file("history.json")

    while True:
        print("\nMenu:")
        print("1. Add product")
        print("2. Remove product")
        print("3. Edit product")
        print("4. Mark product as bought")
        print("5. Display products")
        print("6. Filter products")
        print("7. Display purchase history")
        print("8. Generate statistics")
        print("9. Save and exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter product name: ")
            quantity = int(input("Enter product quantity: "))
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            notes = input("Enter product notes: ")
            product = Product(name, quantity, category, price, notes)
            shopping_list.add_product(product)
        elif choice == "2":
            name = input("Enter the name of the product to remove: ")
            try:
                shopping_list.remove_product(name)
            except ProductNotFoundError as e:
                print(e)
        elif choice == "3":
            name = input("Enter the name of the product to edit: ")
            quantity = input("Enter new quantity (leave blank to keep current): ")
            price = input("Enter new price (leave blank to keep current): ")
            notes = input("Enter new notes (leave blank to keep current): ")
            quantity = int(quantity) if quantity else None
            price = float(price) if price else None
            try:
                shopping_list.edit_product(name, quantity, price, notes)
            except ProductNotFoundError as e:
                print(e)
        elif choice == "4":
            name = input("Enter the name of the product to mark as bought: ")
            try:
                shopping_list.mark_product_as_bought(name)
            except ProductNotFoundError as e:
                print(e)
        elif choice == "5":
            print("Current products:")
            shopping_list.display_products()
        elif choice == "6":
            criterion = input("Enter filter criterion (bought, not bought, category): ")
            try:
                filtered_products = shopping_list.filter_products(criterion)
                print(f"Filtered products ({criterion}):")
                for product in filtered_products:
                    print(product)
            except ValueError as e:
                print(e)
        elif choice == "7":
            print("Purchase history:")
            shopping_list.display_history()
        elif choice == "8":
            stats = shopping_list.generate_statistics()
            print(f"Total spent: {stats['total_spent']}")
            print(f"Average spent: {stats['average_spent']}")
            print(f"Most frequent product: {stats['most_frequent_product']}")
        elif choice == "9":
            shopping_list.write_to_file("shopping_list.json")
            shopping_list.save_history_to_file("history.json")
            print("Shopping list and history saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
