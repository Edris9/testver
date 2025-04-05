# Orderhistorik för E-handelsplattform

## Om Orderhistorik-modulen

Orderhistorik-modulen gör det möjligt för användare att se sina tidigare beställningar. Modulen erbjuder följande funktionalitet:

- Spara nya ordrar med produktdetaljer, antal och priser
- Visa användares tidigare beställningar i kronologisk ordning
- Hantera flera ordrar per användare
- Visa detaljerad information om varje produkt och ordersumma
- Datapersistens genom JSON-lagring

## Implementerade tester

Vi har utvecklat en omfattande testsvit för orderhistorik-modulen:

### Enhetstester (orderhistorik_test.py)
Dessa tester verifierar att enskilda funktioner fungerar korrekt:
- `test_spara_order`: Kontrollerar att en order sparas korrekt i JSON-filen
- `test_visa_orderhistorik_med_ordrar`: Testar att orderhistorik visas korrekt när det finns ordrar
- `test_visa_orderhistorik_utan_ordrar`: Verifierar korrekt hantering när en användare saknar tidigare ordrar

### Integrationstester (orderhistorik_integrationstest.py)
Testar hur funktioner fungerar tillsammans i olika flöden:
- `test_spara_och_visa_orderhistorik`: Testar hela flödet från att spara en order till att visa den
- `test_flera_ordrar_för_samma_användare`: Verifierar korrekt hantering av multipla ordrar

### Acceptanstester (orderhistorik.feature)
BDD-tester som beskriver funktionaliteten ur användarens perspektiv:
- Scenario: Visa tom orderhistorik
- Scenario: Spara en ny order
- Scenario: Visa orderhistorik med en order
- Scenario: Visa orderhistorik med flera ordrar

### Systemtester
Vi försökte implementera systemtester för orderhistorik-modulen, men stötte på utmaningar:
- Testerna var instabila mellan olika operativsystem
- Timing-problem och oförutsägbart beteende vid process-interaktion
- Svårigheter med simulering av användarinmatning

Vi valde därför att fokusera på acceptanstester som ger liknande värde men med större pålitlighet.

## Teststrategier och lärdomar

- **Stegvis testning**: Genom att börja med enhetstest och fortsätta med mer omfattande tester fick vi en systematisk kvalitetssäkring
- **BDD-fördelar**: Gherkin-syntax gjorde testerna lättförståeliga även för icke-tekniska personer
- **Dataisolering**: Varje test använder en separat testfil för att undvika att påverka verklig data
- **Mockning**: Utskrifter mockades för att möjliggöra verifiering av användarmeddelanden