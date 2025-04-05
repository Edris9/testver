import unittest
from unittest.mock import MagicMock
from varukorg import Produkt, Varukorg  # Antag att koden är i filen your_module.py

class TestSystemVarukorgFlowMedMocks(unittest.TestCase):

    def setUp(self):
        """Konfigurera systemet med mock-objekt och initialt tillstånd."""
        self.produkt1 = Produkt(1, "Mock Produkt 1", 100)
        self.produkt2 = Produkt(2, "Mock Produkt 2", 200)

        self.mock_produkt_katalog = MagicMock()
        self.mock_produkt_katalog.hamta_produkt.side_effect = lambda pid: {
            1: self.produkt1,
            2: self.produkt2
        }.get(pid)

        self.mock_lager_system = MagicMock()
        self.mock_lager_system.kontrollera_lager.return_value = True  # Anta att det alltid finns i lager för detta test

        self.mock_sparare = MagicMock()

        self.varukorg = Varukorg(self.mock_produkt_katalog, self.mock_lager_system, self.mock_sparare)

    def test_anvandarflode_lagg_till_andra_antal_ta_bort(self):
        """Simulerar ett användarflöde med mock-objekt."""

        # --- Steg 1: Användaren hittar en produkt och lägger till den i varukorgen ---
        print("\n--- Steg 1: Lägger till produkt ---")
        produkt_id_att_lagga_till = 1
        antal_att_lagga_till = 2
        print(f"Användaren försöker lägga till {antal_att_lagga_till} enheter av produkt med ID {produkt_id_att_lagga_till}.")
        lyckades_lagga_till = self.varukorg.lagg_till(produkt_id_att_lagga_till, antal_att_lagga_till)
        self.assertTrue(lyckades_lagga_till, "Kunde inte lägga till produkten i varukorgen.")
        innehall = self.varukorg.hamta_innehall()
        self.assertIn(self.produkt1, innehall, f"Produkt {self.produkt1.namn} finns inte i varukorgen.")
        self.assertEqual(innehall[self.produkt1], antal_att_lagga_till, f"Fel antal av {self.produkt1.namn} i varukorgen.")
        self.mock_produkt_katalog.hamta_produkt.assert_called_with(produkt_id_att_lagga_till)
        self.mock_lager_system.kontrollera_lager.assert_called_with(produkt_id_att_lagga_till, antal_att_lagga_till)
        print(f"Produkten lades till. Aktuellt innehåll: {innehall}")

        # --- Steg 2: Användaren vill ändra antalet av produkten ---
        print("\n--- Steg 2: Ändrar antal ---")
        nytt_antal = 4
        print(f"Användaren vill ändra antalet av produkt med ID {produkt_id_att_lagga_till} till {nytt_antal}.")
        self.mock_lager_system.kontrollera_lager.return_value = True # Säkerställ att lagret tillåter ändringen
        lyckades_uppdatera = self.varukorg.uppdatera_antal(produkt_id_att_lagga_till, nytt_antal)
        self.assertTrue(lyckades_uppdatera, "Kunde inte uppdatera antalet i varukorgen.")
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall[self.produkt1], nytt_antal, f"Antalet av {self.produkt1.namn} är inte {nytt_antal}.")
        self.mock_lager_system.kontrollera_lager.assert_called_with(produkt_id_att_lagga_till, nytt_antal)
        print(f"Antalet ändrades. Aktuellt innehåll: {innehall}")

        # --- Steg 3: Användaren vill ta bort en del av produkten ---
        print("\n--- Steg 3: Tar bort en del av produkten ---")
        antal_att_ta_bort = 1
        print(f"Användaren vill ta bort {antal_att_ta_bort} enheter av produkt med ID {produkt_id_att_lagga_till}.")
        lyckades_ta_bort = self.varukorg.ta_bort(produkt_id_att_lagga_till, antal_att_ta_bort)
        self.assertTrue(lyckades_ta_bort, "Kunde inte ta bort produkten från varukorgen.")
        innehall = self.varukorg.hamta_innehall()
        self.assertEqual(innehall[self.produkt1], nytt_antal - antal_att_ta_bort, f"Fel antal av {self.produkt1.namn} efter borttagning.")
        print(f"En enhet togs bort. Aktuellt innehåll: {innehall}")

        # --- Steg 4: Användaren vill ta bort hela produkten ---
        print("\n--- Steg 4: Tar bort hela produkten ---")
        antal_att_ta_bort_resterande = innehall[self.produkt1]
        print(f"Användaren vill ta bort de återstående {antal_att_ta_bort_resterande} enheterna av produkt med ID {produkt_id_att_lagga_till}.")
        lyckades_ta_bort_alla = self.varukorg.ta_bort(produkt_id_att_lagga_till, antal_att_ta_bort_resterande)
        self.assertTrue(lyckades_ta_bort_alla, "Kunde inte ta bort alla enheter av produkten.")
        innehall = self.varukorg.hamta_innehall()
        self.assertNotIn(self.produkt1, innehall, f"Produkt {self.produkt1.namn} borde inte längre finnas i varukorgen.")
        print(f"Alla enheter togs bort. Aktuellt innehåll: {innehall}")

        # --- Steg 5: Försöker lägga till en produkt som inte finns ---
        print("\n--- Steg 5: Försöker lägga till en produkt som inte finns ---")
        ogiltigt_produkt_id = 3
        antal_att_forsoka_lagga_till_ogiltig = 1
        print(f"Användaren försöker lägga till {antal_att_forsoka_lagga_till_ogiltig} enheter av produkt med ID {ogiltigt_produkt_id}.")
        self.mock_lager_system.kontrollera_lager.reset_mock()  # Återställ anropshistoriken
        lyckades_lagga_till_ogiltig = self.varukorg.lagg_till(ogiltigt_produkt_id, antal_att_forsoka_lagga_till_ogiltig)
        self.assertFalse(lyckades_lagga_till_ogiltig, "Borde inte kunna lägga till en produkt som inte finns.")
        self.mock_produkt_katalog.hamta_produkt.assert_called_with(ogiltigt_produkt_id)
        self.mock_lager_system.kontrollera_lager.assert_not_called()
        innehall = self.varukorg.hamta_innehall()
        self.assertNotIn(self.produkt2, innehall, "Varukorgen borde fortfarande vara tom.") # Förutsätter att produkt2 inte lades till tidigare
        print(f"Försöket att lägga till en ogiltig produkt misslyckades som förväntat. Aktuellt innehåll: {innehall}")

        # --- Steg 6: Användaren försöker uppdatera antalet på en produkt som inte finns i varukorgen ---
        print("\n--- Steg 6: Försöker uppdatera antalet på en produkt som inte finns i varukorgen ---")
        produkt_id_ej_i_varukorgen = 2
        nytt_antal_ej_i_varukorgen = 3
        print(f"Användaren försöker uppdatera antalet för produkt med ID {produkt_id_ej_i_varukorgen} till {nytt_antal_ej_i_varukorgen}.")
        lyckades_uppdatera_ej_i_varukorgen = self.varukorg.uppdatera_antal(produkt_id_ej_i_varukorgen, nytt_antal_ej_i_varukorgen)
        self.assertFalse(lyckades_uppdatera_ej_i_varukorgen, "Borde inte kunna uppdatera antalet för en produkt som inte finns i varukorgen.")
        self.mock_lager_system.kontrollera_lager.assert_not_called()
        print(f"Försöket att uppdatera en produkt som inte finns i varukorgen misslyckades som förväntat.")

if __name__ == '__main__':
    unittest.main()