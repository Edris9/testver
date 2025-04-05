from behave import given, when, then
from unittest.mock import MagicMock

# --- Setup Mock-objekt ---
mock_varukorg = MagicMock(produkter={})
mock_produkt_katalog = MagicMock()
mock_lager_system = MagicMock()

# --- Temporär lagring av data under testkörningen ---
produkter = {}
totalpris = None
meddelande = None

@given(u'att produkten "{produkt_namn}" med ID {produkt_id:d} och pris {pris:d} finns i katalogen')
def step_impl(context, produkt_namn, produkt_id, pris):
    produkter[produkt_id] = {'namn': produkt_namn, 'pris': pris, 'id': produkt_id}
    mock_produkt_katalog.hamta_produkt.side_effect = lambda pid: produkter.get(pid)

@given(u'att lagret för produkt med ID {produkt_id:d} är {antal:d}')
def step_impl(context, produkt_id, antal):
    mock_lager_system.kontrollera_lager.side_effect = lambda pid, req_antal: pid == produkt_id and req_antal <= antal

@given(u'att jag har en tom varukorg')
def step_impl(context):
    global mock_varukorg
    mock_varukorg.produkter = {}
    global totalpris
    totalpris = None
    global meddelande
    meddelande = None

@given(u'att jag har {antal:d} "{produkt_namn}" i varukorgen')
def step_impl(context, antal, produkt_namn):
    global mock_varukorg
    produkt = next((p for p in produkter.values() if p['namn'] == produkt_namn), None)
    if produkt:
        mock_varukorg.produkter[produkt['id']] = antal

@when(u'jag lägger till {antal:d} "{produkt_namn}" i varukorgen')
def step_impl(context, antal, produkt_namn):
    global mock_varukorg
    global meddelande
    produkt = next((p for p in produkter.values() if p['namn'] == produkt_namn), None)
    if produkt and mock_lager_system.kontrollera_lager(produkt['id'], antal):
        if produkt['id'] in mock_varukorg.produkter:
            mock_varukorg.produkter[produkt['id']] += antal
        else:
            mock_varukorg.produkter[produkt['id']] = antal
    elif not produkt:
        meddelande = f"Produkten '{produkt_namn}' hittades inte."
    else:
        meddelande = f"Inte tillräckligt med lager för '{produkt_namn}'."

@when(u'jag lägger till ytterligare {antal:d} "{produkt_namn}" i varukorgen')
def step_impl(context, antal, produkt_namn):
    step_impl(context, antal, produkt_namn) 

@then(u'ska min varukorg innehålla {antal:d} "{produkt_namn}"')
def step_impl(context, antal, produkt_namn):
    produkt = next((p for p in produkter.values() if p['namn'] == produkt_namn), None)
    assert produkt['id'] in mock_varukorg.produkter
    assert mock_varukorg.produkter[produkt['id']] == antal

@then(u'ska min varukorg innehålla {antal_t1:d} "{produkt_namn_1}" och {antal_t2:d} "{produkt_namn_2}"')
def step_impl(context, antal_t1, produkt_namn_1, antal_t2, produkt_namn_2):
    produkt1 = next((p for p in produkter.values() if p['namn'] == produkt_namn_1), None)
    produkt2 = next((p for p in produkter.values() if p['namn'] == produkt_namn_2), None)
    assert produkt1['id'] in mock_varukorg.produkter
    assert mock_varukorg.produkter[produkt1['id']] == antal_t1
    assert produkt2['id'] in mock_varukorg.produkter
    assert mock_varukorg.produkter[produkt2['id']] == antal_t2

@when(u'jag tar bort {antal:d} "{produkt_namn}" från varukorgen')
def step_impl(context, antal, produkt_namn):
    global mock_varukorg
    produkt = next((p for p in produkter.values() if p['namn'] == produkt_namn), None)
    if produkt and produkt['id'] in mock_varukorg.produkter:
        mock_varukorg.produkter[produkt['id']] -= antal
        if mock_varukorg.produkter[produkt['id']] <= 0:
            del mock_varukorg.produkter[produkt['id']]

@then(u'ska min varukorg vara tom')
def step_impl(context):
    assert not mock_varukorg.produkter

@when(u'jag försöker ta bort {antal:d} "{produkt_namn}" från varukorgen')
def step_impl(context, antal, produkt_namn):
    # Återanvänder ta bort-steget för att simulera försöket
    step_impl(context, antal, produkt_namn)

@when(u'jag beräknar totalpriset')
def step_impl(context):
    global mock_varukorg
    global totalpris
    totalpris = 0
    for produkt_id, antal in mock_varukorg.produkter.items():
        produkt = produkter.get(produkt_id)
        if produkt:
            totalpris += produkt['pris'] * antal

@then(u'ska totalpriset vara {pris:d} kr')
def step_impl(context, pris):
    global totalpris
    assert totalpris == pris

@when(u'jag ändrar antalet av "{produkt_namn}" till {antal:d}')
def step_impl(context, produkt_namn, antal):
    global mock_varukorg
    produkt = next((p for p in produkter.values() if p['namn'] == produkt_namn), None)
    if produkt and mock_lager_system.kontrollera_lager(produkt['id'], antal):
        mock_varukorg.produkter[produkt['id']] = antal
    else:
        global meddelande
        meddelande = f"Inte tillräckligt med lager för '{produkt_namn}'."

@when(u'jag rensar varukorgen')
def step_impl(context):
    global mock_varukorg
    mock_varukorg.produkter = {}

@when(u'jag försöker lägga till 1 "{produkt_namn}" med ID {produkt_id:d} i varukorgen')
def step_impl(context, produkt_namn, produkt_id):
    global mock_varukorg
    produkt = produkter.get(produkt_id)
    if produkt and mock_lager_system.kontrollera_lager(produkt_id, 1):
        if produkt_id in mock_varukorg.produkter:
            mock_varukorg.produkter[produkt_id] += 1
        else:
            mock_varukorg.produkter[produkt_id] = 1
    else:
        global meddelande
        meddelande = f"Produkten med ID {produkt_id} hittades inte eller otillräckligt lager."

@then(u'ska produkten inte läggas till i varukorgen')
def step_impl(context):
    assert not mock_varukorg.produkter  # Enkel kontroll, kan behöva förfinas

@then(u'ett meddelande visas att produkten inte hittades')
def step_impl(context):
    global meddelande
    assert meddelande == "Produkten 'Okänd Produkt' hittades inte."

@then(u'ett meddelande visas att lagret är otillräckligt')
def step_impl(context):
    global meddelande
    assert meddelande == "Inte tillräckligt med lager för 'Blå T-shirt'."



### mer komplexa tester kan läggas till här ###...