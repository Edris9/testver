import unittest
import os
import json
import sys
import subprocess
import time
# Removed unused import StringIO
import orderhistorik
# Removed unused import ORDERHISTORIK_FIL

class SystemTest(unittest.TestCase):
    """Systemtest för orderhistorik-modulen"""
    
    def setUp(self):
        """Körs före varje testmetod."""
        # Använd en testfil för systemtestet
        self.test_fil = "systemtest_orderhistorik.json"
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
    
    def test_program_start_och_avslut(self):
        """Testar att programmet kan starta och avslutas korrekt."""
        # Starta programmet som en separat process
        process = subprocess.Popen(
            [sys.executable, 'orderhistorik.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffering
        )
        
        try:
            # Vänta en kort stund för att programmet ska starta
            time.sleep(0.5)
            
            # Skicka "3" för att välja "Avsluta"
            process.stdin.write("3\n")
            process.stdin.flush()
            
            # Vänta på att processen avslutas (max 2 sekunder)
            process.wait(timeout=2)
            
            # Kontrollera att programmet avslutades korrekt
            self.assertEqual(0, process.returncode, "Programmet avslutades inte korrekt")
            
        except subprocess.TimeoutExpired:
            # Om timeout, tvinga avslut
            process.kill()
            self.fail("Programmet svarade inte eller avslutades inte inom tidsgränsen")
    
    def test_skapa_exempelorder(self):
        """
        Testar att skapa en exempelorder via huvudmenyns gränssnitt.
        Kontrollerar sedan att ordern finns i filen.
        """
        # Starta programmet som en separat process
        process = subprocess.Popen(
            [sys.executable, 'orderhistorik.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffering
        )
        
        try:
            # Vänta en kort stund för att programmet ska starta
            time.sleep(0.5)
            
            process.stdin.write("2\n")  # Välj "Skapa exempelorder"
            process.stdin.write("2\n")  # Välj "Skapa exempelorder"
            process.stdin.flush()
            time.sleep(0.1)
            
            process.stdin.write("systemtestuser\n")  # Ange användarnamn
            time.sleep(0.1)
            
            # Avsluta programmet
            process.stdin.write("3\n")  # Välj "Avsluta"
            process.stdin.flush()
            
            # Vänta på att processen avslutas
            process.wait(timeout=2)
            
            # Kontrollera att ordern sparades i filen
            self.assertTrue(os.path.exists(self.test_fil), "Orderfilen skapades inte")
            
            # Läs in data från filen
            with open(self.test_fil, "r") as f:
                data = json.load(f)
            
            # Kontrollera att användaren finns och har en order
            self.assertIn("systemtestuser", data, "Användaren finns inte i filen")
            self.assertEqual(1, len(data["systemtestuser"]), "Fel antal ordrar sparades")
            
            # Kontrollera att ordern innehåller exempelprodukterna
            order = data["systemtestuser"][0]
            produktnamn = [p["namn"] for p in order["produkter"]]
            self.assertIn("T-shirt", produktnamn, "T-shirt finns inte i ordern")
            self.assertIn("Jeans", produktnamn, "Jeans finns inte i ordern")
            
            # Kontrollera totalsumman
            self.assertEqual(997, order["total_summa"], "Fel totalsumma sparades")
            
        except subprocess.TimeoutExpired:
            # Om timeout, tvinga avslut
            process.kill()
            self.fail("Programmet svarade inte eller avslutades inte inom tidsgränsen")
        except Exception as e:
            # Om något annat går fel, tvinga avslut och rapportera felet
            process.kill()
            self.fail(f"Testet misslyckades: {str(e)}")

if __name__ == '__main__':
    unittest.main()