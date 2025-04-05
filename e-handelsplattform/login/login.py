import os

TEST_ANVANDARDATA_FIL = "test_anvandare.txt"

def registrera(anvandarnamn, losenord, anvandardata_fil=TEST_ANVANDARDATA_FIL):
    if anvandarnamn_finns(anvandarnamn, anvandardata_fil):
        print("Användarnamnet är redan upptaget.")
        return False
    
    with open(anvandardata_fil, "a") as f:
        f.write(f"{anvandarnamn}:{losenord}\n")
    print(f"Användare '{anvandarnamn}' har registrerats.")
    return True

def logga_in(anvandarnamn, losenord, anvandardata_fil=TEST_ANVANDARDATA_FIL, test_mode=False):
    if not os.path.exists(anvandardata_fil):
        print("Felaktigt användarnamn eller lösenord.")
        return False
        
    with open(anvandardata_fil, "r") as f:
        for rad in f:
            if not rad.strip():  # Hoppa över tomma rader
                continue
            lagrat_anvandarnamn, lagrat_losenord = rad.strip().split(":")
            if anvandarnamn == lagrat_anvandarnamn and losenord == lagrat_losenord:
                print(f"Inloggad som '{anvandarnamn}'.")
                if not test_mode:
                    hantera_konto(anvandarnamn)
                return True

    print("Felaktigt användarnamn eller lösenord.")
    return False

def anvandarnamn_finns(anvandarnamn, anvandardata_fil=TEST_ANVANDARDATA_FIL):
    if not os.path.exists(anvandardata_fil):
        return False
    with open(anvandardata_fil, "r") as f:
        for rad in f:
            if not rad.strip():  # Hoppa över tomma rader
                continue
            lagrat_anvandarnamn, _ = rad.strip().split(":")
            if anvandarnamn == lagrat_anvandarnamn:
                return True
    return False


def rensa_testdata(anvandardata_fil=TEST_ANVANDARDATA_FIL):
    if os.path.exists(anvandardata_fil):
        os.remove(anvandardata_fil)

def hantera_konto(aktuell_anvandare):
    while True:
        print("\nKontohantering:")
        print("1. Visa användarnamn")
        print("2. Logga ut")
        val = input("Välj ett alternativ: ")

        if val == "1":
            print(f"Ditt användarnamn är: {aktuell_anvandare}")
        elif val == "2":
            print("Utloggad.")
            break
        else:
            print("Ogiltigt val.")

def huvudmeny():
    while True:
        print("\n--- Inloggningssystem ---")
        print("1. Registrera")
        print("2. Logga in")
        print("3. Avsluta")
        val = input("Välj ett alternativ: ")

        if val == "1":
            anvandarnamn = input("Ange ett användarnamn: ")
            losenord = input("Ange ett lösenord: ")
            registrera(anvandarnamn, losenord)
        elif val == "2":
            anvandarnamn = input("Ange ditt användarnamn: ")
            losenord = input("Ange ditt lösenord: ")
            logga_in(anvandarnamn, losenord)
        elif val == "3":
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val.")

if __name__ == "__main__":
    huvudmeny()