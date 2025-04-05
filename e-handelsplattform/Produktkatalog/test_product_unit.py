import unittest
from product_Catalo import Product, ProductCatalog

class TestProduct(unittest.TestCase):
    
    def test_product_creation(self):
        """Test att en produkt skapas med rätt attribut"""
        product = Product("1", "T-shirt", "En fin t-shirt", 199.99, "Kläder", 10)
        self.assertEqual(product.id, "1")
        self.assertEqual(product.name, "T-shirt")
        self.assertEqual(product.description, "En fin t-shirt")
        self.assertEqual(product.price, 199.99)
        self.assertEqual(product.category, "Kläder")
        self.assertEqual(product.in_stock, 10)

    def test_product_string_representation(self):
        """Test att str() metoden fungerar som förväntat"""
        product = Product("1", "T-shirt", "En fin t-shirt", 199.99, "Kläder", 10)
        self.assertEqual(str(product), "T-shirt (199.99 kr) - Kläder")


class TestProductCatalog(unittest.TestCase):
    
    def setUp(self):
        """Skapa en katalog och några produkter för varje test"""
        self.catalog = ProductCatalog()
        
        self.product1 = Product("1", "T-shirt", "En fin t-shirt", 199.99, "Kläder", 10)
        self.product2 = Product("2", "Jeans", "Blå jeans", 499.99, "Kläder", 5)
        self.product3 = Product("3", "Sneakers", "Vita sneakers", 899.99, "Skor", 3)
        
        self.catalog.add_product(self.product1)
        self.catalog.add_product(self.product2)
        self.catalog.add_product(self.product3)
    
    def test_add_product(self):
        """Test att lägga till en produkt i katalogen"""
        new_product = Product("4", "Keps", "En snygg keps", 149.99, "Accessoarer", 8)
        self.catalog.add_product(new_product)
        
        retrieved_product = self.catalog.get_product("4")
        self.assertEqual(retrieved_product, new_product)
    
    def test_get_product(self):
        """Test att hämta en produkt med ID"""
        product = self.catalog.get_product("2")
        self.assertEqual(product, self.product2)
        
        # Test att hämta en produkt som inte finns
        product = self.catalog.get_product("999")
        self.assertIsNone(product)
    
    def test_search(self):
        """Test att söka efter produkter"""
        # Sök efter "t-shirt" i namn
        results = self.catalog.search("t-shirt")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.product1)
        
        # Sök efter "jeans" i namn
        results = self.catalog.search("jeans")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.product2)
        
        # Sök efter "vita" i beskrivning
        results = self.catalog.search("vita")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.product3)
        
        # Sök efter något som ger flera träffar
        results = self.catalog.search("e")
        self.assertEqual(len(results), 3)
        
        # Sök efter något som inte finns
        results = self.catalog.search("hatt")
        self.assertEqual(len(results), 0)
    
    def test_get_products_by_category(self):
        """Test att hämta produkter i en kategori"""
        # Hämta alla kläder
        results = self.catalog.get_products_by_category("Kläder")
        self.assertEqual(len(results), 2)
        self.assertIn(self.product1, results)
        self.assertIn(self.product2, results)
        
        # Hämta alla skor
        results = self.catalog.get_products_by_category("Skor")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.product3)
        
        # Hämta en kategori som inte finns
        results = self.catalog.get_products_by_category("Elektronik")
        self.assertEqual(len(results), 0)
    
    def test_get_all_products(self):
        """Test att hämta alla produkter"""
        all_products = self.catalog.get_all_products()
        self.assertEqual(len(all_products), 3)
        self.assertIn(self.product1, all_products)
        self.assertIn(self.product2, all_products)
        self.assertIn(self.product3, all_products)


if __name__ == "__main__":
    unittest.main()