# Inloggningssystem

Ett enkelt inloggningssystem i Python med användarhantering och omfattande testsuite.

## Funktioner

- **Registrering**: Användare kan skapa nya konton med användarnamn och lösenord
- **Inloggning**: Användare kan logga in med sina uppgifter
- **Kontohantering**: Inloggade användare kan se sitt användarnamn och logga ut

## Filer

- `login.py` - Huvudprogrammet med alla funktioner för användarhantering
- `enhetstest.py` - Enhetstester för att verifiera att individuella funktioner fungerar korrekt
- `integrationstest.py` - Integrationstester för att verifiera att funktioner fungerar tillsammans
- `acceptanstest.py` - Acceptanstester med Behave för att verifiera att systemet uppfyller användarkraven

## Testning

Systemet innehåller flera nivåer av tester:

### Enhetstester
Testar enskilda funktioner isolerat:
```
python enhetstest.py
```

### Integrationstester
Testar hur funktioner fungerar tillsammans:
```
python integrationstest.py
```

### Acceptanstester (BDD)
Testar systemet från användarens perspektiv med hjälp av Behave:
```
cd features
behave
```

### Systemtester
Vi valde att inte köra systemtester eftersom de är mindre pålitliga på olika plattformar och miljöer. Systemtester kräver att köra programmet som en separat process, vilket kan vara problematiskt på grund av timing och operativsystemsberoenden. Istället fokuserade vi på acceptanstester som ger liknande täckning men med större pålitlighet.

## Teststrategier

- **Enhetstester**: Fokuserar på individuella funktioner med mock för externa beroenden
- **Integrationstester**: Kontrollerar att funktioner samverkar korrekt
- **Acceptanstester**: Verifierar att systemet uppfyller användarnas krav med scenarios skrivna i Gherkin-syntax