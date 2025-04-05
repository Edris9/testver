from behave import given, when, then, step
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Lägg till sökvägen så att orderhistorik kan importeras
current_dir = os.path.dirname(os.path.abspath(__file__))
features_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(features_dir)
sys.path.append(project_dir)

import orderhistorik
from orderhistorik import spara_order, visa_orderhistorik, ladda_alla_ordrar

# Testfil för orderhistorik
TEST_FIL = "test_behave_orderhistorik.json"

@given('systemet är redo att ta emot ordrar')
def step_impl(context):
    # Byt till testfilen
    context.original_fil = orderhistorik.ORDERHISTORIK_FIL
    orderhistorik.ORDERHISTORIK_FIL = TEST_FIL
    
    # Ta bort testfilen om den finns
    if os.path.exists(TEST_FIL):
        os.remove(TEST_FIL)
    
    # Initiera mockning av print
    context.print_patcher = patch('builtins.print')
    context.mock_print = context.print_patcher.start()
    context.meddelanden = []
    
    def samla_meddelanden(*args):
        message = ' '.join(str(arg) for arg in args)
        context.meddelanden.append(message)
    
    context.mock_print.side_effect = samla_meddelanden

@given('användaren "{username}" har inga tidigare beställningar')
def step_impl(context, username):
    # Byt till testfilen
    context.original_fil = orderhistorik.ORDERHISTORIK_FIL
    orderhistorik.ORDERHISTORIK_FIL = TEST_FIL
    
    # Skapa en tom fil eller töm befintlig fil
    with open(TEST_FIL, "w") as f:
        json.dump({}, f)
    
    # Spara användarnamnet för senare steg
    context.username = username
    
    # Initiera mockning av print
    context.print_patcher = patch('builtins.print')
    context.mock_print = context.print_patcher.start()
    context.meddelanden = []
    
    def samla_meddelanden(*args):
        message = ' '.join(str(arg) for arg in args)
        context.meddelanden.append(message)
    
    context.mock_print.side_effect = samla_meddelanden

@given('användaren "{username}" har en tidigare beställning')
def step_impl(context, username):
    # Byt till testfilen
    context.original_fil = orderhistorik.ORDERHISTORIK_FIL
    orderhistorik.ORDERHISTORIK_FIL = TEST_FIL
    
    # Skapa en testorder
    with open(TEST_FIL, "w") as f:
        json.dump({
            username: [
                {
                    "datum": "2025-04-05 14:30",
                    "produkter": [
                        {"namn": "T-shirt", "antal": 2, "pris": 199}
                    ],
                    "total_summa": 398
                }
            ]
        }, f)
    
    # Spara användarnamnet för senare steg
    context.username = username
    
    # Initiera mockning av print
    context.print_patcher = patch('builtins.print')
    context.mock_print = context.print_patcher.start()
    context.meddelanden = []
    
    def samla_meddelanden(*args):
        message = ' '.join(str(arg) for arg in args)
        context.meddelanden.append(message)
    
    context.mock_print.side_effect = samla_meddelanden

@given('användaren "{username}" har flera tidigare beställningar')
def step_impl(context, username):
    # Byt till testfilen
    context.original_fil = orderhistorik.ORDERHISTORIK_FIL
    orderhistorik.ORDERHISTORIK_FIL = TEST_FIL
    
    # Skapa flera testordrar
    with open(TEST_FIL, "w") as f:
        json.dump({
            username: [
                {
                    "datum": "2025-04-01 10:15",
                    "produkter": [
                        {"namn": "T-shirt", "antal": 1, "pris": 199}
                    ],
                    "total_summa": 199
                },
                {
                    "datum": "2025-04-05 14:30",
                    "produkter": [
                        {"namn": "Jeans", "antal": 1, "pris": 599},
                        {"namn": "Skjorta", "antal": 2, "pris": 249}
                    ],
                    "total_summa": 1097
                }
            ]
        }, f)
    
    # Spara användarnamnet för senare steg
    context.username = username
    
    # Initiera mockning av print
    context.print_patcher = patch('builtins.print')
    context.mock_print = context.print_patcher.start()
    context.meddelanden = []
    
    def samla_meddelanden(*args):
        message = ' '.join(str(arg) for arg in args)
        context.meddelanden.append(message)
    
    context.mock_print.side_effect = samla_meddelanden

@when('användaren begär att se sin orderhistorik')
def step_impl(context):
    visa_orderhistorik(context.username)

@when('användaren "{username}" lägger en order med följande produkter:')
def step_impl(context, username):
    # Konvertera tabellen till produkter
    produkter = []
    for row in context.table:
        produkt = {
            "namn": row["namn"],
            "antal": int(row["antal"]),
            "pris": int(row["pris"])
        }
        produkter.append(produkt)
    
    # Spara för senare steg
    context.username = username
    context.produkter = produkter

@when('orderns totalsumma är {summa} kr')
def step_impl(context, summa):
    context.total_summa = int(summa)

@then('ska systemet visa att inga ordrar hittades')
def step_impl(context):
    expected_message = f"Inga tidigare ordrar hittades för {context.username}."
    assert any(expected_message in msg for msg in context.meddelanden), \
        f"Förväntade meddelandet '{expected_message}' hittades inte"

@then('ska ordern sparas i systemet')
def step_impl(context):
    # Spara ordern
    spara_order(context.username, context.produkter, context.total_summa)
    
    # Kontrollera att ordern har sparats
    assert os.path.exists(TEST_FIL), "Orderfilen skapades inte"
    
    # Läs in data från filen
    with open(TEST_FIL, "r") as f:
        data = json.load(f)
    
    # Kontrollera att användarens data finns
    assert context.username in data, f"Användaren {context.username} finns inte i filen"
    assert len(data[context.username]) > 0, "Inga ordrar sparades för användaren"
    
    # Kontrollera att produkterna finns
    order = data[context.username][-1]  # Senaste ordern
    assert "produkter" in order, "Ordern innehåller inga produkter"
    assert len(order["produkter"]) == len(context.produkter), "Fel antal produkter i ordern"
    
    # Kontrollera totalsumman
    assert order["total_summa"] == context.total_summa, "Fel totalsumma i ordern"

@then('användaren ska få en bekräftelse')
def step_impl(context):
    expected_message = f"Order sparad för {context.username}."
    assert any(expected_message in msg for msg in context.meddelanden), \
        f"Förväntade meddelandet '{expected_message}' hittades inte"

@then('ska systemet visa orderinformationen')
def step_impl(context):
    expected_header = f"=== Orderhistorik för {context.username} ==="
    assert any(expected_header in msg for msg in context.meddelanden), \
        f"Orderhistorikens rubrik '{expected_header}' hittades inte"

@then('orderinformationen ska innehålla produktnamn och priser')
def step_impl(context):
    # Läs in data för att kontrollera vad som borde visas
    with open(TEST_FIL, "r") as f:
        data = json.load(f)
    
    # Kontrollera att produktinformation visas
    produkter = data[context.username][0]["produkter"]
    for produkt in produkter:
        assert any(produkt["namn"] in msg for msg in context.meddelanden), \
            f"Produktnamnet '{produkt['namn']}' hittades inte i utskriften"
        assert any(str(produkt["pris"]) in msg for msg in context.meddelanden), \
            f"Produktpriset '{produkt['pris']}' hittades inte i utskriften"

@then('orderinformationen ska visa totalsumman')
def step_impl(context):
    # Läs in data för att kontrollera vad som borde visas
    with open(TEST_FIL, "r") as f:
        data = json.load(f)
    
    # Kontrollera att totalsumman visas
    total = data[context.username][0]["total_summa"]
    assert any(f"Totalsumma: {total}" in msg for msg in context.meddelanden), \
        f"Totalsumman '{total}' hittades inte i utskriften"

@then('ska systemet visa alla ordrar i kronologisk ordning')
def step_impl(context):
    # Kontrollera att flera ordrar visas
    order_count = 0
    for msg in context.meddelanden:
        if "Order #" in msg:
            order_count += 1
    
    # Läs in data för att kontrollera hur många ordrar som borde visas
    with open(TEST_FIL, "r") as f:
        data = json.load(f)
    
    expected_count = len(data[context.username])
    assert order_count == expected_count, \
        f"Fel antal ordrar visades. Förväntade {expected_count}, fick {order_count}"

@then('varje order ska ha sitt eget ordernummer')
def step_impl(context):
    # Kontrollera att ordernummer visas
    order_numbers = []
    for msg in context.meddelanden:
        if "Order #" in msg:
            # Extrahera ordernumret
            parts = msg.split("Order #")
            if len(parts) > 1:
                number_part = parts[1].split(" ")[0]
                try:
                    order_numbers.append(int(number_part))
                except ValueError:
                    pass
    
    # Kontrollera att vi har unika, sekventiella ordernummer
    assert len(order_numbers) > 0, "Inga ordernummer hittades"
    assert sorted(order_numbers) == list(range(min(order_numbers), max(order_numbers) + 1)), \
        "Ordernumren är inte sekventiella"

def after_scenario(context, scenario):
    # Återställ originalfilnamnet
    if hasattr(context, 'original_fil'):
        orderhistorik.ORDERHISTORIK_FIL = context.original_fil
    
    # Ta bort testfilen
    if os.path.exists(TEST_FIL):
        os.remove(TEST_FIL)
    
    # Stoppa mockning
    if hasattr(context, 'print_patcher'):
        context.print_patcher.stop()