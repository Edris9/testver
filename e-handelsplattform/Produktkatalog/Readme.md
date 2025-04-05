# Produktkatalog Testning

## Funktionella Tester

### Enhetstest (test_product_unit.py)
- Testar att produktklassen fungerar korrekt
- Testar sökfunktioner, filtrering på kategori
- Testar att hämta, lägga till och uppdatera produkter
- Fokuserar på isolerade komponenter för att säkerställa korrekt funktion

### Integrationstest (test_product_integration.py)
- Testar integration mellan produkt och databas
- Verifierar korrekt lagring och hämtning av produktdata
- Använder en mock-databas för att simulera databasbeteende
- Säkerställer att olika komponenter fungerar tillsammans

### Systemtest (test_product_system.py)
- Testar hela produktkatalogen som ett system
- Simulerar användarscenarion för sökning och produktvisning
- Fokuserar på flöden snarare än enskilda funktioner
- Verifierar kategorinavigering och produkttillgänglighet

### Acceptanstest (product_catalog.feature)
- BDD-tester skrivna i Gherkin-syntax
- Verifierar användarkrav från affärsperspektiv
- Testar sökning, kategoribläddring och produktdetaljer
- Säkerställer att funktionaliteten möter användarnas behov

## Icke-funktionella Tester

### Prestandatester för Produktkatalog
- Sökhastighet vid stor produktkatalog
- Responstider för filtrering och kategorisortering
- Databasbelastning vid samtidiga sökningar
- Testa med tidtagning och benchmark-verktyg

### Säkerhetstester för Produktkatalog
- SQL-injektion i sökfunktioner
- Validering av produktinformation
- Behörighetshantering för produktadministration
- Cross-site scripting (XSS) i produktbeskrivningar

### Användbarhetstester för Produktkatalog
- Sökgränssnittets användarvänlighet
- Produktfiltrering och sortering
- Navigering mellan produktkategorier
- Produktdetaljvisning

## Prioritering
- **Högst**: Korrekt produktsökning (affärskritisk funktion)
- **Medel**: Kategorinavigering och filtrering
- **Medel**: Prestandatester för stora produktkataloger
- **Lägre**: Säkerhetstester för produktvisning