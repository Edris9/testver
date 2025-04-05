import unittest
from unittest.mock import MagicMock
from varukorg import Produkt, Varukorg 

class TestVarukorg(unittest.TestCase):

    def setUp(self):
        """Skapa mock-objekt och en varukorgsinstans för varje test."""
        self.mock_produkt_katalog = MagicMock()
        self.mock_lager_system = MagicMock()
        self.mock_sparare = MagicMock()
        self.varukorg = Varukorg(self.mock_produkt_katalog, self.mock_lager_system, self.mock_sparare)

        # Skapa några exempelprodukter för mock-katalogen
        self.produkt1 = Produkt(1, "Testprodukt 1", 100)
        self.produkt2 = Produkt(2, "Testprodukt 2", 200)
        self.mock_produkt_katalog.hamta_produkt.side_effect = lambda pid: {
            1: self.produkt1,
            2: self.produkt2
        }.get(pid)

    def test_lagg_till_produkt_lyckas(self):
        """Testa att lägga till en produkt i varukorgen lyckas."""
        self.mock_lager_system.kontrollera_lager.return_value = True
        resultat = self.varukorg.lagg_till(1)
        self.assertTrue(resultat)
        self.assertEqual(self.varukorg.produkter, {1: 1})
        self.mock_produkt_katalog.hamta_produkt.assert_called_once_with(1)
        self.mock_lager_system.kontrollera_lager.assert_called_once_with(1, 1)

    def test_lagg_till_produkt_finns_redan(self):
        """Testa att öka antalet om produkten redan finns i varukorgen."""
        self.varukorg.produkter = {1: 2}
        self.mock_lager_system.kontrollera_lager.return_value = True
        resultat = self.varukorg.lagg_till(1, 3)
        self.assertTrue(resultat)
        self.assertEqual(self.varukorg.produkter, {1: 5})
        self.mock_produkt_katalog.hamta_produkt.assert_called_once_with(1)
        self.mock_lager_system.kontrollera_lager.assert_called_once_with(1, 3)

    def test_lagg_till_produkt_ej_i_lager(self):
        """Testa att lägga till misslyckas om produkten inte finns i lager."""
        self.mock_lager_system.kontrollera_lager.return_value = False
        resultat = self.varukorg.lagg_till(1)
        self.assertFalse(resultat)
        self.assertEqual(self.varukorg.produkter, {})
        self.mock_produkt_katalog.hamta_produkt.assert_called_once_with(1)
        self.mock_lager_system.kontrollera_lager.assert_called_once_with(1, 1)

    def test_lagg_till_produkt_ej_i_katalog(self):
        """Testa att lägga till misslyckas om produkten inte finns i katalogen."""
        resultat = self.varukorg.lagg_till(3)  # Produkt-ID 3 finns inte i mock-katalogen
        self.assertFalse(resultat)
        self.assertEqual(self.varukorg.produkter, {})
        self.mock_produkt_katalog.hamta_produkt.assert_called_once_with(3)
        self.mock_lager_system.kontrollera_lager.assert_not_called()

    def test_ta_bort_produkt_lyckas(self):
        """Testa att ta bort en befintlig produkt från varukorgen."""
        self.varukorg.produkter = {1: 3}
        resultat = self.varukorg.ta_bort(1, 2)
        self.assertTrue(resultat)
        self.assertEqual(self.varukorg.produkter, {1: 1})

    def test_ta_bort_mer_an_finns(self):
        """Testa att ta bort fler än vad som finns i varukorgen."""
        self.varukorg.produkter = {1: 1}
        resultat = self.varukorg.ta_bort(1, 2)
        self.assertTrue(resultat)
        self.assertEqual(self.varukorg.produkter, {})

    def test_ta_bort_produkt_inte_i_varukorgen(self):
        """Testa att ta bort en produkt som inte finns i varukorgen."""
        resultat = self.varukorg.ta_bort(3)
        self.assertFalse(resultat)
        self.assertEqual(self.varukorg.produkter, {})

    def test_hamta_innehall(self):
        """Testa att hämta innehållet i varukorgen korrekt."""
        self.varukorg.produkter = {1: 2, 2: 1}
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall, {self.produkt1: 2, self.produkt2: 1})
        self.mock_produkt_katalog.hamta_produkt.assert_any_call(1)
        self.mock_produkt_katalog.hamta_produkt.assert_any_call(2)
        self.assertEqual(self.mock_produkt_katalog.hamta_produkt.call_count, 2)

    def test_berakna_totalpris(self):
        """Testa att beräkna totalpriset korrekt."""
        self.varukorg.produkter = {1: 2, 2: 1}
        totalpris = self.varukorg.berakna_totalpris()
        self.assertEqual(totalpris, (self.produkt1.pris * 2) + (self.produkt2.pris * 1))
        self.mock_produkt_katalog.hamta_produkt.assert_any_call(1)
        self.mock_produkt_katalog.hamta_produkt.assert_any_call(2)
        self.assertEqual(self.mock_produkt_katalog.hamta_produkt.call_count, 2)

    def test_uppdatera_antal_ok(self):
        """Testa att uppdatera antalet av en produkt i varukorgen."""
        self.varukorg.produkter = {1: 2}
        self.mock_lager_system.kontrollera_lager.return_value = True
        resultat = self.varukorg.uppdatera_antal(1, 5)
        self.assertTrue(resultat)
        self.assertEqual(self.varukorg.produkter, {1: 5})
        self.mock_lager_system.kontrollera_lager.assert_called_once_with(1, 5)

    def test_uppdatera_antal_till_noll_eller_mindre(self):
        """Testa att uppdatera antalet till noll eller mindre tar bort produkten."""
        self.varukorg.produkter = {1: 2}
        resultat1 = self.varukorg.uppdatera_antal(1, 0)
        self.assertTrue(resultat1)
        self.assertEqual(self.varukorg.produkter, {})

        self.varukorg.produkter = {2: 1}
        resultat2 = self.varukorg.uppdatera_antal(2, -1)
        self.assertTrue(resultat2)
        self.assertEqual(self.varukorg.produkter, {})
        self.mock_lager_system.kontrollera_lager.assert_not_called() # Borde inte kallas vid borttagning

    def test_uppdatera_antal_produkt_ej_i_varukorgen(self):
        """Testa att uppdatera antalet för en produkt som inte finns i varukorgen."""
        self.mock_lager_system.kontrollera_lager.return_value = True
        resultat = self.varukorg.uppdatera_antal(3, 2)
        self.assertFalse(resultat)
        self.assertEqual(self.varukorg.produkter, {})
        self.mock_lager_system.kontrollera_lager.assert_not_called()

    def test_uppdatera_antal_ej_i_lager(self):
        """Testa att uppdatera antalet misslyckas om det nya antalet inte finns i lager."""
        self.varukorg.produkter = {1: 1}
        self.mock_lager_system.kontrollera_lager.return_value = False
        resultat = self.varukorg.uppdatera_antal(1, 3)
        self.assertFalse(resultat)
        self.assertEqual(self.varukorg.produkter, {1: 1})
        self.mock_lager_system.kontrollera_lager.assert_called_once_with(1, 3)

    def test_rensa(self):
        """Testa att rensa varukorgen tömmer den."""
        self.varukorg.produkter = {1: 2, 2: 1}
        self.varukorg.rensa()
        self.assertEqual(self.varukorg.produkter, {})

    def test_spara_varukorg(self):
        """Testa att spara varukorgen anropar spararens metod."""
        session_id = "anvandare123"
        self.varukorg.produkter = {1: 2, 2: 1}
        self.varukorg.spara(session_id)
        self.mock_sparare.spara_varukorg.assert_called_once_with(session_id, {1: 2, 2: 1})

    def test_spara_varukorg_ingen_sparare(self):
        """Testa att spara kastar NotImplementedError om ingen sparare är konfigurerad."""
        varukorg_utan_sparare = Varukorg(self.mock_produkt_katalog, self.mock_lager_system)
        session_id = "anvandare123"
        with self.assertRaises(NotImplementedError):
            varukorg_utan_sparare.spara(session_id)

    def test_ladda_varukorg(self):
        """Testa att ladda varukorgen anropar spararens metod och uppdaterar innehållet."""
        session_id = "anvandare123"
        sparad_data = {3: 5, 4: 1}
        self.mock_sparare.hamta_varukorg.return_value = sparad_data
        self.varukorg.ladda(session_id)
        self.assertEqual(self.varukorg.produkter, sparad_data)
        self.mock_sparare.hamta_varukorg.assert_called_once_with(session_id)

    def test_ladda_varukorg_ingen_sparare(self):
        """Testa att ladda kastar NotImplementedError om ingen sparare är konfigurerad."""
        varukorg_utan_sparare = Varukorg(self.mock_produkt_katalog, self.mock_lager_system)
        session_id = "anvandare123"
        with self.assertRaises(NotImplementedError):
            varukorg_utan_sparare.ladda(session_id)

    def test_ladda_varukorg_ingen_data(self):
        """Testa att ladda inte gör något om spararen inte har någon data för sessionen."""
        session_id = "anvandare123"
        self.mock_sparare.hamta_varukorg.return_value = None
        self.varukorg.ladda(session_id)
        self.assertEqual(self.varukorg.produkter, {}) # Förväntar sig att varukorgen förblir tom om inget laddas

if __name__ == '__main__':
    unittest.main()