import unittest
import os
import json
from unittest.mock import patch
import orderhistorik
from orderhistorik import spara_order, visa_orderhistorik, ladda_alla_ordrar, ORDERHISTORIK_FIL

class IntegrationTest(unittest.TestCase):
    """Integrationstest för orderhistorik-modulen"""
    
    def setUp(self):
        """Körs före varje testmetod."""
        # Använd en testfil istället för den riktiga filen
        self.test_fil = "test_integration_orderhistorik.json"
        self.original_fil = orderhistorik.ORDERHISTORIK_FIL
        orderhistorik.ORDERHISTORIK_FIL = self.test_fil
        
        # Ta bort testfilen om den redan finns
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)
    
    def tearDown(self):
        """Körs efter varje testmetod."""
        # Återställ originalfilnamnet
        orderhistorik.ORDERHISTORIK_FIL = self.original_fil
        
        # Ta bort testfilen
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)
    
    @patch('builtins.print')
    def test_spara_och_visa_orderhistorik(self, mock_print):
        """
        Testar hela flödet där en order sparas och sedan visas i orderhistoriken.
        Detta är ett integrationstest som testar att funktionerna fungerar tillsammans.
        """
        # 1. Testdata
        användarnamn = "testuser"
        produkter = [
            {"namn": "T-shirt", "antal": 2, "pris": 199},
            {"namn": "Jeans", "antal": 1, "pris": 499}
        ]
        total_summa = 897
        
        # 2. Spara ordern
        spara_order(användarnamn, produkter, total_summa)
        
        # Kontrollera att ordern sparats korrekt i filen
        self.assertTrue(os.path.exists(self.test_fil), "Filen skapades inte")
        
        # 3. Rensa mock för att bara fånga utskrifter från visa_orderhistorik
        mock_print.reset_mock()
        
        # 4. Visa orderhistoriken
        visa_orderhistorik(användarnamn)
        
        # 5. Verifiera att orderhistoriken visades korrekt
        # Kontrollera att rubriken visades
        mock_print.assert_any_call(f"\n=== Orderhistorik för {användarnamn} ===")
        
        # Kontrollera att produktinformationen visades
        produkter_visade = False
        totalsumma_visad = False
        
        for call in mock_print.call_args_list:
            args, _ = call
            if args and isinstance(args[0], str):
                if "T-shirt" in args[0] and "199" in args[0]:
                    produkter_visade = True
                if f"Totalsumma: {total_summa}" in args[0]:
                    totalsumma_visad = True
        
        self.assertTrue(produkter_visade, "Produktinformationen visades inte")
        self.assertTrue(totalsumma_visad, "Totalsumman visades inte")
    
    @patch('builtins.print')
    def test_flera_ordrar_för_samma_användare(self, mock_print):
        """
        Testar att flera ordrar för samma användare hanteras korrekt.
        Detta integrerar sparande och visande av ordrar i en sekvens.
        """
        # 1. Testdata för första ordern
        användarnamn = "multiuser"
        produkter1 = [{"namn": "Produkt1", "antal": 1, "pris": 100}]
        total_summa1 = 100
        
        # 2. Spara första ordern
        spara_order(användarnamn, produkter1, total_summa1)
        
        # 3. Testdata för andra ordern
        produkter2 = [{"namn": "Produkt2", "antal": 2, "pris": 200}]
        total_summa2 = 400
        
        # 4. Spara andra ordern
        spara_order(användarnamn, produkter2, total_summa2)
        
        # 5. Rensa mock
        mock_print.reset_mock()
        
        # 6. Visa orderhistoriken
        visa_orderhistorik(användarnamn)
        
        # 7. Verifiera att båda ordrarna visades
        produkt1_visad = False
        produkt2_visad = False
        
        for call in mock_print.call_args_list:
            args, _ = call
            if args and isinstance(args[0], str):
                if "Produkt1" in args[0]:
                    produkt1_visad = True
                if "Produkt2" in args[0]:
                    produkt2_visad = True
        
        self.assertTrue(produkt1_visad, "Första ordern visades inte")
        self.assertTrue(produkt2_visad, "Andra ordern visades inte")
        
        # 8. Kontrollera även i lagrad data att båda ordrarna finns
        all_data = ladda_alla_ordrar()
        self.assertEqual(2, len(all_data[användarnamn]), "Fel antal ordrar sparades")

if __name__ == '__main__':
    unittest.main()
