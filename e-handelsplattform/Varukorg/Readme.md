För att testa varukorgen behövs flera olika testtyper:

1. **Enhetstest**
   - Testar isolerade funktioner som att lägga till, ta bort och uppdatera produkter i varukorgen
   - Verifierar att prisberäkningar och kvantitetsuppdateringar fungerar korrekt
   - **Varför**: För att säkerställa att varje enskild funktion i varukorgen fungerar korrekt utan beroenden

2. **Integrationstest**
   - Testar hur varukorgen interagerar med produktkatalogen och lagersystemet
   - Verifierar att varukorgsdata sparas korrekt mellan olika sessioner
   - **Varför**: För att säkerställa att varukorgen fungerar tillsammans med andra delar av systemet

3. **Systemtest**
   - Testar hela flödet från att hitta en produkt till att lägga den i varukorgen och göra ändringar
   - **Varför**: För att verifiera att användarflödet fungerar från start till slut

4. **Acceptanstest**
   - BDD-testscenarier för typiska varukorgsbeteenden som användare förväntar sig
   - **Varför**: För att bekräfta att funktionaliteten möter användarkraven

5. **Gränssnittstest**
   - Testar att UI-komponenter för varukorgen fungerar som förväntat
   - **Varför**: För att säkerställa att användare kan interagera med varukorgen på ett intuitivt sätt

Särskilt viktigt för varukorgen är att testa kantfall som:
- Ändra kvantiteter till negativa värden eller noll
- Lägga till produkter som är slut i lager
- Uppdatera samma produkt flera gånger
- Beräkning av totalbelopp med rabatter

Varukorgen är en särskilt kritisk del av e-handelsplattformen eftersom den direkt påverkar konverteringsgraden och därmed affärsresultatet.



i denna jag har simulerat : 
systemtest simulerade framgångsrikt ett användarflöde som inkluderade:

Att lägga till en produkt i varukorgen.
Att ändra antalet av produkten.
Att ta bort en del av produkten.
Att ta bort hela produkten.
Att försöka lägga till en produkt som inte finns i produktkatalogen (vilket misslyckades som förväntat).
Att försöka uppdatera antalet för en produkt som inte finns i varukorgen (vilket också misslyckades som förväntat).