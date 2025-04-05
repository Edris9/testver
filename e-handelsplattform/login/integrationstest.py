import unittest
import os
from io import StringIO
from unittest.mock import patch
import sys
from login import registrera, logga_in, anvandarnamn_finns, TEST_ANVANDARDATA_FIL, rensa_testdata

class IntegrationTest(unittest.TestCase):
    """Integrationstest för inloggningssystemet"""
    
    def setUp(self):
        """Körs före varje testmetod."""
        rensa_testdata()
        # Skapa testfilen om den inte finns
        if not os.path.exists(TEST_ANVANDARDATA_FIL):
            open(TEST_ANVANDARDATA_FIL, 'a').close()
    
    def tearDown(self):
        """Körs efter varje testmetod."""
        rensa_testdata()
    
    @patch('builtins.print')
    def test_hela_flödet(self, mock_print):
        """Test av hela användarflödet: registrering -> inloggning"""
        
        # Steg 1: Registrera en användare
        registrera('testuser', 'lösenord123')
        
        # Steg 2: Kontrollera att användaren finns
        self.assertTrue(anvandarnamn_finns('testuser'))
        
        # Steg 3: Testa inloggning med rätt uppgifter
        logga_in('testuser', 'lösenord123', test_mode=True)
        
        # Kontrollera att inloggningen lyckades
        # (vi kollar att "Inloggad som" har skrivits ut någon gång)
        inloggad = False
        for call in mock_print.call_args_list:
            args, _ = call
            if args and "Inloggad som 'testuser'" in args[0]:
                inloggad = True
                break
        
        self.assertTrue(inloggad, "Inloggningen misslyckades")
        
    @patch('builtins.print')
    def test_felaktigt_flöde(self, mock_print):
        """Test av felhantering: registrering -> felaktig inloggning"""
        
        # Steg 1: Registrera en användare
        registrera('testuser', 'lösenord123')
        
        # Steg 2: Försök logga in med fel lösenord
        logga_in('testuser', 'fel_lösenord', test_mode=True)
        
        # Kontrollera att felmeddelande visades
        fel_meddelande = False
        for call in mock_print.call_args_list:
            args, _ = call
            if args and "Felaktigt användarnamn eller lösenord" in args[0]:
                fel_meddelande = True
                break
        
        self.assertTrue(fel_meddelande, "Inget felmeddelande visades vid felaktig inloggning")

if __name__ == '__main__':
    unittest.main()