from unittest.mock import MagicMock

class Produkt:
    def __init__(self, id, namn, pris):
        self.id = id
        self.namn = namn
        self.pris = pris

    def __eq__(self, other):
        if not isinstance(other, Produkt):
            return NotImplemented
        return self.id == other.id and self.namn == other.namn and self.pris == other.pris

    def __hash__(self):
        return hash((self.id, self.namn, self.pris))

class Varukorg:
    def __init__(self, produkt_katalog, lager_system, sparare=None):
        self.produkter = {}  # {produkt_id: antal}
        self.produkt_katalog = produkt_katalog
        self.lager_system = lager_system
        self.sparare = sparare

    def lagg_till(self, produkt_id, antal=1):
        produkt = self.produkt_katalog.hamta_produkt(produkt_id)
        if produkt and self.lager_system.kontrollera_lager(produkt_id, antal):
            if produkt_id in self.produkter:
                self.produkter[produkt_id] += antal
            else:
                self.produkter[produkt_id] = antal
            return True
        return False

    def ta_bort(self, produkt_id, antal=1):
        if produkt_id in self.produkter:
            antal_att_ta_bort = min(self.produkter[produkt_id], antal)
            self.produkter[produkt_id] -= antal_att_ta_bort
            if self.produkter[produkt_id] <= 0:
                del self.produkter[produkt_id]
            return True
        return False

    def hamta_innehall(self):
        innehall = {}
        for produkt_id, antal in self.produkter.items():
            produkt = self.produkt_katalog.hamta_produkt(produkt_id)
            if produkt:
                innehall[produkt] = antal
        return innehall

    def berakna_totalpris(self):
        totalpris = 0
        for produkt_id, antal in self.produkter.items():
            produkt = self.produkt_katalog.hamta_produkt(produkt_id)
            if produkt:
                totalpris += produkt.pris * antal
        return totalpris

    def uppdatera_antal(self, produkt_id, antal):
        if produkt_id in self.produkter:
            if antal > 0 and self.lager_system.kontrollera_lager(produkt_id, antal):
                self.produkter[produkt_id] = antal
                return True
            elif antal <= 0:
                del self.produkter[produkt_id]
                return True
        return False

    def rensa(self):
        self.produkter = {}

    def spara(self, session_id):
        if self.sparare:
            self.sparare.spara_varukorg(session_id, self.produkter)
        else:
            raise NotImplementedError("Ingen sparare har konfigurerats för varukorgen.")

    def ladda(self, session_id):
        if self.sparare:
            inladen_data = self.sparare.hamta_varukorg(session_id)
            if inladen_data:
                self.produkter = inladen_data
        else:
            raise NotImplementedError("Ingen sparare har konfigurerats för varukorgen.")

# --- Mock-objekt för beroenden ---
class MockProduktKatalog:
    def __init__(self, produkter):
        self.produkter = {p.id: p for p in produkter}
    def hamta_produkt(self, produkt_id):
        return self.produkter.get(produkt_id)

class MockLagerSystem:
    def kontrollera_lager(self, produkt_id, antal):
        # Simulerar att alla produkter alltid finns i lager
        return True

class MockVarukorgsSparare:
    def __init__(self):
        self.sparad_data = {}
    def spara_varukorg(self, session_id, varukorg_data):
        self.sparad_data[session_id] = varukorg_data
    def hamta_varukorg(self, session_id):
        return self.sparad_data.get(session_id)

if __name__ == "__main__":
    # Skapa några exempelprodukter
    produkt1 = Produkt(1, "T-shirt", 200)
    produkt2 = Produkt(2, "Jeans", 500)
    produkt3 = Produkt(3, "Skor", 700)

    # Skapa en mock-produktkatalog
    katalog = MockProduktKatalog([produkt1, produkt2, produkt3])

    # Skapa en mock-lagersystem
    lager = MockLagerSystem()

    # Skapa en mock-sparare
    sparare = MockVarukorgsSparare()

    # Skapa en varukorg med de mockade beroendena
    min_varukorg = Varukorg(katalog, lager, sparare)

    while True:
        print("\n--- Varukorg ---")
        print("1. Lägg till vara")
        print("2. Visa varukorg")
        print("3. Ta bort vara")
        print("4. Beräkna totalpris")
        print("5. Spara varukorg")
        print("6. Ladda varukorg")
        print("7. Avsluta")

        val = input("Välj ett alternativ: ")

        if val == "1":
            try:
                produkt_id = int(input("Ange produkt-ID att lägga till: "))
                antal = int(input("Ange antal: "))
                if min_varukorg.lagg_till(produkt_id, antal):
                    produkt = katalog.hamta_produkt(produkt_id)
                    if produkt:
                        print(f"{antal} st av '{produkt.namn}' har lagts till i varukorgen.")
                    else:
                        print(f"Produkt med ID {produkt_id} hittades inte.")
                else:
                    print(f"Kunde inte lägga till produkt {produkt_id}. Kontrollera om produkten finns.")
            except ValueError:
                print("Ogiltig inmatning. Ange ett heltal för produkt-ID och antal.")

        elif val == "2":
            innehall = min_varukorg.hamta_innehall()
            if innehall:
                print("\n--- Innehåll i varukorgen ---")
                for produkt, antal in innehall.items():
                    print(f"{produkt.namn} (ID: {produkt.id}), Pris: {produkt.pris} kr, Antal: {antal}")
            else:
                print("Varukorgen är tom.")

        elif val == "3":
            try:
                produkt_id = int(input("Ange produkt-ID att ta bort: "))
                antal = int(input("Ange antal att ta bort (lämna tomt för att ta bort 1): ") or 1)
                if min_varukorg.ta_bort(produkt_id, antal):
                    produkt = katalog.hamta_produkt(produkt_id)
                    if produkt:
                        print(f"{antal} st av '{produkt.namn}' har tagits bort från varukorgen.")
                    else:
                        print(f"Produkt med ID {produkt_id} hittades inte.")
                else:
                    print(f"Produkten med ID {produkt_id} finns inte i varukorgen.")
            except ValueError:
                print("Ogiltig inmatning. Ange ett heltal för produkt-ID och antal.")

        elif val == "4":
            totalpris = min_varukorg.berakna_totalpris()
            print(f"Totalpris i varukorgen: {totalpris} kr")

        elif val == "5":
            session_id = input("Ange ett session-ID för att spara varukorgen: ")
            try:
                min_varukorg.spara(session_id)
                print(f"Varukorgen har sparats för session: {session_id}")
            except NotImplementedError as e:
                print(e)

        elif val == "6":
            session_id = input("Ange session-ID att ladda varukorgen från: ")
            try:
                min_varukorg.ladda(session_id)
                print(f"Varukorgen har laddats från session: {session_id}")
            except NotImplementedError as e:
                print(e)

        elif val == "7":
            print("Tack för att du handlade!")
            break

        else:
            print("Ogiltigt val. Försök igen.")