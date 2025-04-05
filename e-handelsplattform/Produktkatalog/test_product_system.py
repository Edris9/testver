import unittest
from product_Catalo import Product, ProductCatalog

class TestProductSystem(unittest.TestCase):
    
    def setUp(self):
        # Skapa en produktkatalog med några produkter
        self.catalog = ProductCatalog()
        
        # Lägg till några produkter
        products = [
            Product("1", "T-shirt", "Fin t-shirt", 199, "Kläder", 10),
            Product("2", "Jeans", "Blå jeans", 499, "Kläder", 5),
            Product("3", "Löparskor", "Snabba skor", 899, "Skor", 3)
        ]
        
        for product in products:
            self.catalog.add_product(product)
            
    def test_user_search_flow(self):
        # Simulera en användarsökning efter kläder
        results = self.catalog.search("t-shirt")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "T-shirt")
        
        # Simulera användare som tittar på detaljer för en produkt
        product = self.catalog.get_product("1")
        self.assertEqual(product.price, 199)
        self.assertEqual(product.in_stock, 10)
        
    def test_category_browsing(self):
        # Simulera användare som bläddrar i kategorier
        clothes = self.catalog.get_products_by_category("Kläder")
        self.assertEqual(len(clothes), 2)
        
        shoes = self.catalog.get_products_by_category("Skor")
        self.assertEqual(len(shoes), 1)
        self.assertEqual(shoes[0].name, "Löparskor")
        
    def test_product_availability(self):
        # Kontrollera att lager visas korrekt
        product = self.catalog.get_product("3")
        self.assertEqual(product.in_stock, 3)
        

if __name__ == "__main__":
    unittest.main()