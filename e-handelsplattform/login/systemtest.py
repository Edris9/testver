"""
Acceptanstest för inloggningssystemet
Testar systemet från användarens perspektiv för att säkerställa att det
uppfyller användarnas förväntningar och krav.
"""

import unittest
from unittest.mock import patch
import os
import io
from login import registrera, logga_in, anvandarnamn_finns, TEST_ANVANDARDATA_FIL, rensa_testdata, huvudmeny

class AcceptansTest(unittest.TestCase):
    """Acceptanstest för att verifiera att systemet uppfyller användarnas behov"""
    
    def setUp(self):
        """Körs före varje testmetod."""
        rensa_testdata()
        # Skapa testfilen om den inte finns
        if not os.path.exists(TEST_ANVANDARDATA_FIL):
            open(TEST_ANVANDARDATA_FIL, 'a').close()
    
    def tearDown(self):
        """Körs efter varje testmetod."""
        rensa_testdata()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_användarscenario_registrering_och_inloggning(self, mock_print, mock_input):
        """
        Acceptanstest: Användaren ska kunna registrera sig och sedan logga in
        """
        # Simulera användarens inmatning för hela scenariot
        mock_input.side_effect = [
            "1",            # Välj registrera
            "testanvändare", # Ange användarnamn
            "lösenord123",  # Ange lösenord
            "2",            # Välj logga in
            "testanvändare", # Ange användarnamn för inloggning
            "lösenord123",  # Ange lösenord för inloggning
            "2",            # I kontohantering, välj logga ut
            "3"             # I huvudmenyn, välj avsluta
        ]
        
        # Kör huvudmenyn
        huvudmeny()
        
        # Verifiera att registrering och inloggning lyckades
        registrering_lyckades = False
        inloggning_lyckades = False
        utloggning_lyckades = False
        
        # Kontrollera alla utskrifter för att hitta bekräftelsemeddelanden
        for call in mock_print.call_args_list:
            args = call[0]
            if args and isinstance(args[0], str):
                if "har registrerats" in args[0]:
                    registrering_lyckades = True
                elif "Inloggad som" in args[0]:
                    inloggning_lyckades = True
                elif "Utloggad" in args[0]:
                    utloggning_lyckades = True
        
        # Kontrollera att alla steg i scenariot lyckades
        self.assertTrue(registrering_lyckades, "Registreringen misslyckades")
        self.assertTrue(inloggning_lyckades, "Inloggningen misslyckades")
        self.assertTrue(utloggning_lyckades, "Utloggningen misslyckades")
        
        # Verifiera också att användaren finns i systemet
        self.assertTrue(anvandarnamn_finns("testanvändare"), 
                       "Användaren kunde inte hittas i systemet")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_felhantering_vid_inloggning(self, mock_print, mock_input):
        """
        Acceptanstest: Systemet ska hantera felaktiga inloggningsuppgifter korrekt
        """
        # Registrera först en användare
        registrera("testanvändare", "rätt_lösenord")
        
        # Simulera inloggningsförsök med fel lösenord
        mock_input.side_effect = [
            "2",            # Välj logga in
            "testanvändare", # Ange användarnamn
            "fel_lösenord", # Ange fel lösenord
            "3"             # Välj avsluta
        ]
        
        # Kör huvudmenyn
        huvudmeny()
        
        # Verifiera att ett felmeddelande visades
        felmeddelande_visades = False
        for call in mock_print.call_args_list:
            args = call[0]
            if args and isinstance(args[0], str) and "Felaktigt användarnamn eller lösenord" in args[0]:
                felmeddelande_visades = True
                break
        
        self.assertTrue(felmeddelande_visades, 
                       "Inget felmeddelande visades vid felaktiga inloggningsuppgifter")

if __name__ == '__main__':
    unittest.main()