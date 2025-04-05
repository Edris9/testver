from behave import given, when, then
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

# Förbättrad import för login-modulen
# Detta lägger till föräldrakatalogen till sökvägen så att 'login' kan importeras
current_dir = os.path.dirname(os.path.abspath(__file__))
features_dir = os.path.dirname(current_dir)
login_dir = os.path.dirname(features_dir)
sys.path.append(login_dir)

# Nu kan vi importera från login-modulen
import login
from login import registrera, logga_in, anvandarnamn_finns, TEST_ANVANDARDATA_FIL, rensa_testdata

@given('systemet är igång')
def step_impl(context):
    # Rensa testdata innan vi börjar
    rensa_testdata()
    # Skapa en tom fil om den inte finns
    if not os.path.exists(TEST_ANVANDARDATA_FIL):
        open(TEST_ANVANDARDATA_FIL, 'a').close()
    # Spara mockar i context för senare användning
    context.stdout_patcher = patch('builtins.print')
    context.mock_stdout = context.stdout_patcher.start()
    context.messages = []
    
    # Spara alla utskrifter för att kunna söka i dem senare
    def fake_print(*args):
        message = ' '.join(str(arg) for arg in args)
        context.messages.append(message)
    
    context.mock_stdout.side_effect = fake_print

@given('en användare med namn "{username}" och lösenord "{password}" finns')
def step_impl(context, username, password):
    # Rensa testdata innan vi börjar
    rensa_testdata()
    # Skapa en tom fil om den inte finns
    if not os.path.exists(TEST_ANVANDARDATA_FIL):
        open(TEST_ANVANDARDATA_FIL, 'a').close()
        
    # Spara mockar i context för senare användning
    if not hasattr(context, 'stdout_patcher'):
        context.stdout_patcher = patch('builtins.print')
        context.mock_stdout = context.stdout_patcher.start()
        context.messages = []
        
        # Spara alla utskrifter för att kunna söka i dem senare
        def fake_print(*args):
            message = ' '.join(str(arg) for arg in args)
            context.messages.append(message)
        
        context.mock_stdout.side_effect = fake_print
    
    # Registrera användaren direkt
    with open(TEST_ANVANDARDATA_FIL, "a") as f:
        f.write(f"{username}:{password}\n")
    
    # Verifiera att användaren finns
    assert anvandarnamn_finns(username) == True

@when('användaren väljer att registrera sig')
def step_impl(context):
    # Spara för framtida steg
    context.action = "registrera"

@when('användaren väljer att logga in')
def step_impl(context):
    # Spara för framtida steg
    context.action = "logga_in"

@when('anger användarnamn "{username}"')
def step_impl(context, username):
    context.username = username

@when('anger lösenord "{password}"')
def step_impl(context, password):
    context.password = password
    
    # Utför den faktiska åtgärden baserat på vad användaren valde
    if context.action == "registrera":
        context.result = registrera(context.username, context.password)
    elif context.action == "logga_in":
        context.result = logga_in(context.username, context.password, test_mode=True)

@then('ska användaren bli registrerad')
def step_impl(context):
    assert anvandarnamn_finns(context.username) == True, f"Användaren {context.username} registrerades inte"

@then('ska användaren bli inloggad')
def step_impl(context):
    assert context.result == True, "Användaren loggades inte in"

@then('ska användaren inte bli inloggad')
def step_impl(context):
    assert context.result == False, "Användaren loggades in när den inte borde ha gjort det"

@then('systemet ska visa "{message}"')
def step_impl(context, message):
    found = False
    for msg in context.messages:
        if message in msg:
            found = True
            break
    
    assert found, f"Meddelandet '{message}' hittades inte i utskrifterna: {context.messages}"

def after_scenario(context, scenario):
    # Rensa testdata efter varje scenario
    rensa_testdata()
    
    # Stoppa patchern om den startades
    if hasattr(context, 'stdout_patcher'):
        context.stdout_patcher.stop()