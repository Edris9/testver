class Product:
    """En enkel produkt i katalogen"""
    
    def __init__(self, id, name, description, price, category, in_stock=0):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.in_stock = in_stock
    
    def __str__(self):
        return f"{self.name} ({self.price} kr) - {self.category}"


class ProductCatalog:
    """En enkel produktkatalog"""
    
    def __init__(self):
        self.products = {}  
    
    def add_product(self, product):
        """Lägg till en produkt i katalogen"""
        self.products[product.id] = product
    
    def get_product(self, product_id):
        """Hämta en produkt med dess ID"""
        return self.products.get(product_id)
    
    def search(self, keyword):
        """Sök efter produkter baserat på namn eller beskrivning"""
        keyword = keyword.lower()
        results = []
        
        for product in self.products.values():
            if keyword in product.name.lower() or keyword in product.description.lower():
                results.append(product)
        
        return results
    
    def get_products_by_category(self, category):
        """Hämta alla produkter i en kategori"""
        return [p for p in self.products.values() if p.category == category]
    
    def get_all_products(self):
        """Hämta alla produkter i katalogen"""
        return list(self.products.values())

# running example
catalog = ProductCatalog()
catalog.add_product(Product(1, "Laptop", "En kraftfull laptop", 9999, "Elektronik", 10))
catalog.add_product(Product(2, "Mobiltelefon", "En smart mobiltelefon", 5999, "Elektronik", 20))
catalog.add_product(Product(3, "Kaffe", "Ett paket kaffe", 49, "Livsmedel", 100))
catalog.add_product(Product(4, "Te", "Ett paket te", 39, "Livsmedel", 50))
catalog.add_product(Product(5, "Bok", "En intressant bok", 199, "Böcker", 30))
catalog.add_product(Product(6, "Penna", "En bläckpenna", 19, "Kontor", 200))
catalog.add_product(Product(7, "Anteckningsblock", "Ett anteckningsblock", 29, "Kontor", 150))
catalog.add_product(Product(8, "Skrivbord", "Ett skrivbord", 1999, "Möbler", 5))
catalog.add_product(Product(9, "Stol", "En bekväm stol", 899, "Möbler", 10))
catalog.add_product(Product(10, "Säng", "En bekväm säng", 4999, "Möbler", 2))


# Sök efter produkter
print("Sökresultat för 'kaffe':")
for product in catalog.search("kaffe"):
    print(product)

print("\nSökresultat för 'stol':")
for product in catalog.search("stol"):
    print(product)

# Hämta produkter i en kategori
print("\nProdukter i kategori 'Elektronik':")
for product in catalog.get_products_by_category("Elektronik"):
    print(product)

# Hämta alla produkter i katalogen
print("\nAlla produkter i katalogen:")
for product in catalog.get_all_products():
    print(product)
# Hämta en specifik produkt

product = catalog.get_product(5)
if product:
    print(f"\nHämtad produkt: {product}")
else:
    print("\nProdukt med ID 1 hittades inte i katalogen.")