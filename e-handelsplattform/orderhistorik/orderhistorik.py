import os
import json
from datetime import datetime

# Filnamn för att lagra orderhistorik
ORDERHISTORIK_FIL = "orderhistorik.json"

def spara_order(användarnamn, produkter, total_summa):
    """
    Sparar en ny order för en användare.
    
    Args:
        användarnamn: Användarens namn
        produkter: Lista av produkter som beställts (lista av dictionaries)
        total_summa: Totalsumman för ordern
    """
    # Skapa en ny order
    order = {
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "produkter": produkter,
        "total_summa": total_summa
    }
    
    # Ladda befintliga ordrar
    alla_ordrar = ladda_alla_ordrar()
    
    # Lägg till den nya ordern för användaren
    if användarnamn not in alla_ordrar:
        alla_ordrar[användarnamn] = []
    
    alla_ordrar[användarnamn].append(order)
    
    # Spara alla ordrar
    with open(ORDERHISTORIK_FIL, "w") as f:
        json.dump(alla_ordrar, f, indent=4)
    
    print(f"Order sparad för {användarnamn}.")

def ladda_alla_ordrar():
    """Laddar alla användares ordrar från fil."""
    if not os.path.exists(ORDERHISTORIK_FIL):
        return {}
    
    try:
        with open(ORDERHISTORIK_FIL, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Om filen är skadad, returnera en tom dictionary
        return {}

def visa_orderhistorik(användarnamn):
    """
    Visar orderhistorik för en specifik användare.
    
    Args:
        användarnamn: Användarens namn
    """
    alla_ordrar = ladda_alla_ordrar()
    
    if användarnamn not in alla_ordrar or not alla_ordrar[användarnamn]:
        print(f"Inga tidigare ordrar hittades för {användarnamn}.")
        return
    
    print(f"\n=== Orderhistorik för {användarnamn} ===")
    
    for i, order in enumerate(alla_ordrar[användarnamn], 1):
        print(f"\nOrder #{i} - {order['datum']}")
        print("Produkter:")
        for produkt in order['produkter']:
            print(f"  - {produkt['namn']} ({produkt['antal']} st): {produkt['pris']} kr")
        print(f"Totalsumma: {order['total_summa']} kr")
    
    print("=" * 40)

def huvudmeny():
    """Huvudmeny för orderhistorik-funktionen."""
    while True:
        print("\n--- Orderhistorik ---")
        print("1. Visa orderhistorik")
        print("2. Skapa exempelorder (demo)")
        print("3. Avsluta")
        
        val = input("Välj ett alternativ: ")
        
        if val == "1":
            användarnamn = input("Ange ditt användarnamn: ")
            visa_orderhistorik(användarnamn)
        elif val == "2":
            # Demo: Skapa en exempelorder
            användarnamn = input("Ange ditt användarnamn: ")
            exempel_produkter = [
                {"namn": "T-shirt", "antal": 2, "pris": 199},
                {"namn": "Jeans", "antal": 1, "pris": 599}
            ]
            spara_order(användarnamn, exempel_produkter, 997)
            print("Exempelorder skapad!")
        elif val == "3":
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val.")

if __name__ == "__main__":
    huvudmeny()