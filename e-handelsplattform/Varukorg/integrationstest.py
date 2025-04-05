import unittest
from varukorg import Produkt, Varukorg 

class EnkelProduktKatalog:
    def __init__(self, produkter):
        self.produkter = {p.id: p for p in produkter}
    def hamta_produkt(self, produkt_id):
        return self.produkter.get(produkt_id)

class EnkelLagerSystem:
    def __init__(self, lager_saldo):
        self.lager_saldo = lager_saldo
    def kontrollera_lager(self, produkt_id, antal):
        return self.lager_saldo.get(produkt_id, 0) >= antal
    def uppdatera_lager(self, produkt_id, antal_andring):
        if produkt_id in self.lager_saldo:
            self.lager_saldo[produkt_id] += antal_andring

class InMemoryVarukorgsSparare:
    def __init__(self):
        self.sparad_data = {}
    def spara_varukorg(self, session_id, varukorg_data):
        self.sparad_data[session_id] = varukorg_data.copy()  
    def hamta_varukorg(self, session_id):
        return self.sparad_data.get(session_id)

class TestVarukorgIntegration(unittest.TestCase):

    def setUp(self):
        """Skapa riktiga instanser av beroenden och varukorgen."""
        self.produkt1 = Produkt(1, "Integrationsprodukt 1", 150)
        self.produkt2 = Produkt(2, "Integrationsprodukt 2", 250)
        self.produkt_katalog = EnkelProduktKatalog([self.produkt1, self.produkt2])
        self.lager_system = EnkelLagerSystem({1: 10, 2: 5})
        self.sparare = InMemoryVarukorgsSparare()
        self.varukorg = Varukorg(self.produkt_katalog, self.lager_system, self.sparare)

    def test_lagg_till_och_hamta_innehall(self):
        """Testa att lägga till produkter och sedan hämta innehållet korrekt."""
        self.assertTrue(self.varukorg.lagg_till(1, 3))
        self.assertTrue(self.varukorg.lagg_till(2, 1))
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall, {self.produkt1: 3, self.produkt2: 1})

    def test_lagg_till_och_berakna_totalpris(self):
        """Testa att lägga till produkter och beräkna totalpriset korrekt."""
        self.assertTrue(self.varukorg.lagg_till(1, 2))
        self.assertTrue(self.varukorg.lagg_till(2, 2))
        totalpris = self.varukorg.berakna_totalpris()
        self.assertEqual(totalpris, (150 * 2) + (250 * 2))

    def test_lagg_till_otillrackligt_lager(self):
        """Testa att lägga till misslyckas om det inte finns tillräckligt med lager."""
        self.assertFalse(self.varukorg.lagg_till(1, 15))
        self.assertEqual(self.varukorg.hamta_innehall(), {})

    def test_ta_bort_och_kontrollera_innehall(self):
        """Testa att ta bort produkter och kontrollera innehållet."""
        self.varukorg.lagg_till(1, 5)
        self.assertTrue(self.varukorg.ta_bort(1, 2))
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall, {self.produkt1: 3})

    def test_spara_och_ladda_varukorg(self):
        """Testa att spara varukorgen och sedan ladda den korrekt."""
        self.varukorg.lagg_till(1, 4)
        self.varukorg.lagg_till(2, 1)
        session_id = "test_session"
        self.varukorg.spara(session_id)

        ny_varukorg = Varukorg(self.produkt_katalog, self.lager_system, self.sparare)
        ny_varukorg.ladda(session_id)
        innehall = ny_varukorg.hamta_innehall()
        self.assertEqual(innehall, {self.produkt1: 4, self.produkt2: 1})

    def test_uppdatera_antal_med_lagerkontroll(self):
        """Testa att uppdatera antalet respekterar lagersaldot."""
        self.varukorg.lagg_till(1, 2)
        self.assertTrue(self.varukorg.uppdatera_antal(1, 8))
        self.assertFalse(self.varukorg.uppdatera_antal(1, 12)) # Överskrider lagret (10)
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall, {self.produkt1: 8})

if __name__ == '__main__':
    unittest.main()