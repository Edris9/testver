import unittest
import json
import os
from product_Catalo import Product, ProductCatalog

class MockDatabase:
    """En enkel mock av en databas för att testa integrationen"""
    
    def __init__(self, db_file="test_products.json"):
        self.db_file = db_file
        self.products = {}
        
        # Skapa en tom databasfil om den inte finns
        if not os.path.exists(db_file):
            with open(db_file, 'w') as f:
                json.dump({}, f)
        else:
            self.load()
    
    def load(self):
        """Ladda produkter från JSON-fil"""
        try:
            with open(self.db_file, 'r') as f:
                self.products = json.load(f)
        except:
            self.products = {}
    
    def save(self):
        """Spara produkter till JSON-fil"""
        with open(self.db_file, 'w') as f:
            json.dump(self.products, f)
    
    def add_product(self, product):
        """Lägg till en produkt i databasen"""
        self.products[product.id] = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': product.category,
            'in_stock': product.in_stock
        }
        self.save()
    
    def get_all_products(self):
        """Hämta alla produkter från databasen"""
        return self.products
    
    def clear(self):
        """Rensa databasen"""
        self.products = {}
        self.save()


class TestProductIntegration(unittest.TestCase):
    
    def setUp(self):
        # Skapa database mock och produktkatalog
        self.db = MockDatabase()
        self.db.clear()  # Rensa databasen före varje test
        self.catalog = ProductCatalog()
        
        # Lägg till några produkter i databasen
        products = [
            Product("1", "T-shirt", "En vit t-shirt", 199, "Kläder", 10),
            Product("2", "Jeans", "Blå jeans", 499, "Kläder", 5)
        ]
        
        for product in products:
            self.db.add_product(product)
    
    def test_load_from_database(self):
        """Testa att ladda produkter från databasen till katalogen"""
        # Hämta produkter från databasen
        db_products = self.db.get_all_products()
        
        # Lägg till produkterna i katalogen
        for product_id, product_data in db_products.items():
            product = Product(
                product_data['id'],
                product_data['name'],
                product_data['description'],
                product_data['price'],
                product_data['category'],
                product_data['in_stock']
            )
            self.catalog.add_product(product)
        
        # Kontrollera att alla produkter laddades korrekt
        self.assertEqual(len(self.catalog.get_all_products()), 2)
        
        # Kontrollera att vi kan söka efter produkterna
        results = self.catalog.search("t-shirt")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "T-shirt")
    
    def test_save_to_database(self):
        """Testa att spara en ny produkt till databasen och sedan hämta den"""
        # Skapa en ny produkt
        new_product = Product("3", "Sneakers", "Vita sneakers", 899, "Skor", 3)
        
        # Lägg till i katalogen
        self.catalog.add_product(new_product)
        
        # Lägg till i databasen
        self.db.add_product(new_product)
        
        # Kontrollera att produkten finns i databasen
        db_products = self.db.get_all_products()
        self.assertIn("3", db_products)
        self.assertEqual(db_products["3"]["name"], "Sneakers")
        
    def tearDown(self):
        """Rensa upp efter testerna"""
        self.db.clear()
        if os.path.exists(self.db.db_file):
            os.remove(self.db.db_file)


if __name__ == "__main__":
    unittest.main()