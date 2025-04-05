import unittest
from unittest.mock import patch
import io
import os
import sys
from login import registrera, logga_in, anvandarnamn_finns, TEST_ANVANDARDATA_FIL, rensa_testdata

class TestLogin(unittest.TestCase):

    def setUp(self):
        """Körs före varje testmetod."""
        rensa_testdata()
        # Skapa filen om den inte finns
        if not os.path.exists(TEST_ANVANDARDATA_FIL):
            open(TEST_ANVANDARDATA_FIL, 'a').close()

    def tearDown(self):
        """Körs efter varje testmetod."""
        rensa_testdata()

    @patch('builtins.print')  # Mocka print-funktionen direkt
    def test_registrera_ny_anvandare(self, mock_print):
        registrera('testuser', 'testpass', TEST_ANVANDARDATA_FIL)
        mock_print.assert_called_with("Användare 'testuser' har registrerats.")
        self.assertTrue(anvandarnamn_finns('testuser', TEST_ANVANDARDATA_FIL))

    @patch('builtins.print')  # Mocka print-funktionen direkt
    def test_registrera_befintlig_anvandare(self, mock_print):
        # Registrera en användare först
        with open(TEST_ANVANDARDATA_FIL, "a") as f:
            f.write("testuser:testpass\n")

        # Försök registrera samma användare igen
        registrera('testuser', 'annatpass', TEST_ANVANDARDATA_FIL)
        mock_print.assert_called_with("Användarnamnet är redan upptaget.")
        self.assertEqual(self._count_lines(TEST_ANVANDARDATA_FIL), 1)  # Kontrollera att ingen ny rad lades till

    @patch('builtins.print')  # Mocka print-funktionen direkt
    def test_logga_in_korrekta_uppgifter(self, mock_print):
        # Skapa en testanvändare
        with open(TEST_ANVANDARDATA_FIL, "a") as f:
            f.write("testuser:testpass\n")

        # Testa inloggning utan att anropa hantera_konto
        logga_in('testuser', 'testpass', TEST_ANVANDARDATA_FIL, test_mode=True)
        mock_print.assert_called_with("Inloggad som 'testuser'.")

    @patch('builtins.print')  # Mocka print-funktionen direkt
    def test_logga_in_felaktiga_uppgifter(self, mock_print):
        # Skapa en testanvändare
        with open(TEST_ANVANDARDATA_FIL, "a") as f:
            f.write("testuser:testpass\n")

        logga_in('fel_user', 'fel_pass', TEST_ANVANDARDATA_FIL, test_mode=True)
        mock_print.assert_called_with("Felaktigt användarnamn eller lösenord.")

    def _count_lines(self, filnamn):
        """Hjälpfunktion för att räkna rader i en fil."""
        try:
            with open(filnamn, 'r') as f:
                return sum(1 for line in f)
        except FileNotFoundError:
            return 0

if __name__ == '__main__':
    unittest.main()