import unittest
from unittest.mock import patch
import os
import json
from orderhistorik import spara_order, visa_orderhistorik, ladda_alla_ordrar, ORDERHISTORIK_FIL

class TestOrderhistorik(unittest.TestCase):
    
    def setUp(self):
        """Körs före varje testmetod."""
        # Säkerställ att vi använder en testfil och inte påverkar befintliga data
        self.test_fil = "test_orderhistorik.json"
        # Spara originalvärdet för att kunna återställa senare
        self.original_fil = ORDERHISTORIK_FIL
        # Ersätt den globala konstanten med vår testfil
        orderhistorik.ORDERHISTORIK_FIL = self.test_fil
        # Ta bort eventuella gamla testfiler
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)
    
    def tearDown(self):
        """Körs efter varje testmetod."""
        # Återställ den ursprungliga filnamnskonstanten
        orderhistorik.ORDERHISTORIK_FIL = self.original_fil
        # Ta bort testfilen
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)
    
    @patch('builtins.print')
    def test_spara_order(self, mock_print):
        """Testar att spara en order fungerar korrekt."""
        # Testdata
        användarnamn = "testuser"
        produkter = [{"namn": "Produkt1", "antal": 2, "pris": 100}]
        total_summa = 200
        
        # Spara en order
        spara_order(användarnamn, produkter, total_summa)
        
        # Verifiera att ordern sparades
        self.assertTrue(os.path.exists(self.test_fil), "Orderfilen skapades inte")
        
        # Läs in innehållet i filen
        with open(self.test_fil, "r") as f:
            data = json.load(f)
        
        # Kontrollera att användaren och ordern finns med
        self.assertIn(användarnamn, data, "Användaren finns inte i filen")
        self.assertEqual(1, len(data[användarnamn]), "Fel antal ordrar sparade")
        self.assertEqual(total_summa, data[användarnamn][0]["total_summa"], "Fel totalsumma sparad")
        
        # Kontrollera att rätt meddelande skrevs ut
        mock_print.assert_called_with(f"Order sparad för {användarnamn}.")
    
    @patch('builtins.print')
    def test_visa_orderhistorik_med_ordrar(self, mock_print):
        """Testar att visa orderhistorik för en användare med ordrar."""
        # Skapa testdata
        testdata = {
            "testuser": [
                {
                    "datum": "2025-04-05 12:00",
                    "produkter": [{"namn": "Produkt1", "antal": 2, "pris": 100}],
                    "total_summa": 200
                }
            ]
        }
        
        # Spara testdata i filen
        with open(self.test_fil, "w") as f:
            json.dump(testdata, f)
        
        # Visa orderhistorik
        visa_orderhistorik("testuser")
        
        # Verifiera att rätt information visades
        mock_print.assert_any_call("\n=== Orderhistorik för testuser ===")
        
        # Kontrollera att någon rad innehåller totalsumman
        totalsumma_visad = False
        for call in mock_print.call_args_list:
            args, _ = call
            if args and "Totalsumma: 200 kr" in args[0]:
                totalsumma_visad = True
                break
        
        self.assertTrue(totalsumma_visad, "Totalsumman visades inte")
    
    @patch('builtins.print')
    def test_visa_orderhistorik_utan_ordrar(self, mock_print):
        """Testar att visa orderhistorik för en användare utan ordrar."""
        # Skapa en tom fil
        with open(self.test_fil, "w") as f:
            json.dump({}, f)
        
        # Visa orderhistorik för en användare som inte har ordrar
        visa_orderhistorik("saknas")
        
        # Verifiera att meddelandet visades
        mock_print.assert_called_with("Inga tidigare ordrar hittades för saknas.")

if __name__ == '__main__':
    import orderhistorik  # Importera modulen för att kunna modifiera konstanten
    unittest.main()