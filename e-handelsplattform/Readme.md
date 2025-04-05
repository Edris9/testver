# Testtyper för e-handelsplattform

## Funktionella tester:

1. **Produktkatalog**:
   - Testa sökfunktion, filtrering och produktvisning
   - Produktkategorier och navigationstester
   - Produktdetaljvisning och datakorrekthet

2. **Varukorg**:
   - Testa att lägga till/ta bort produkter
   - Uppdatera kvantitet och prisberäkning
   - Validera rabatter och delsummor

3. **Kassa**:
   - Testa betalningsflöde
   - Validering av adress/betalningsinformation
   - Orderbekräftelse och kvittopresentation

4. **Användarhantering**:
   - Testa registrering, inloggning, lösenordsåterställning
   - Kontouppdateringar och profilhantering
   - Rättighetshantering och sessioner

5. **Orderhistorik**:
   - Testa att beställningar visas korrekt med rätt information
   - Orderstatusvisning och uppdateringar
   - Filtreringsfunktioner för orderhistorik

## Icke-funktionella tester:

1. **Prestanda**:
   - Lasttester, stresstester (särskilt för produktkatalog och kassa)
   - Responstidsmätningar för kritiska sidor
   - Databasprestandatest med stora volymer
   - Skalbarhetstester under toppar

2. **Säkerhet**:
   - Penetrationstester, dataskyddstester
   - Testning av autentisering och auktorisering
   - Input-validering för att förhindra injektionsattacker
   - Betalningssäkerhetstester (PCI DSS-compliance)
   - GDPR-compliance tester

3. **Användbarhet**:
   - Användarupplevelse på olika enheter
   - Tillgänglighetstester (WCAG)
   - Navigeringstester
   - Konverteringsmätningar för nyckelfunktioner

4. **Kompabilitet**:
   - Testa i olika webbläsare och enheter
   - Operativsystemkompatibilitet
   - Skärmupplösningar och responsivitet

## Testnivåer implementering:

### Enhetstester
- Verifierar att individuella komponenter fungerar isolerat
- Testar gränsfall och felhantering
- Fokuserar på teknisk korrekthet

### Integrationstester
- Testar integration mellan moduler (produktkatalog/databas)
- Verifierar dataflöde mellan komponenter
- Testar synkronisering (t.ex. varukorg/lagersaldo)

### Systemtester
- Simulerar hela användarflöden genom systemet
- Testar end-to-end funktionalitet
- Fokuserar på helhetsbeteende

### Acceptanstester
- BDD-scenarier för typiska användarflöden (Gherkin)
- Verifiera att affärsregler uppfylls
- Säkerställer att systemet möter kundernas förväntningar

## Prioritering av tester:

### Högsta prioritet
1. **Betalningsfunktionalitet** - Direkt koppling till intäkter och kundförtroende
2. **Varukorgsfunktionalitet** - Kritisk för konvertering
3. **Säkerhetstester** - Kritiska för kundförtroende och regelefterlevnad

### Medelhög prioritet
4. **Produktkatalogsökning** - Viktigt för att kunder ska hitta produkter
5. **Användarhantering** - Viktigt för kundrelationer
6. **Prestandatester** - Påverkar användarupplevelse och konvertering

### Lägre prioritet
7. **Orderhistorik** - Användbart men inte affärskritiskt
8. **Kompabilitetstester** - Kan hanteras iterativt
9. **Icke-kritiska användbarhetstester** - Kan förbättras över tid

Denna prioritering säkerställer att de mest affärskritiska funktionerna testas först och grundligast, vilket ger störst affärsvärde.