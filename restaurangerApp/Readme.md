# Testplan för matbeställningsapplikation

## 1. Användarregistrering och inloggning

### Testnivå
**Rekommenderad testnivå: Enhetstest och integrationstest**

*Motivering:* 
- Enhetstest för validering av användardata
- Integrationstest för att verifiera koppling till externa tjänster som Facebook

### Testmetod
**Rekommenderad testmetod: White-box och black-box**

*Motivering:*
- White-box för att testa säker lösenordshantering
- Black-box för att testa användarflöden och felhantering

### Enkel testkod (Python)
```python
# Enhetstest för e-postvalidering
def test_email_validation():
    assert validate_email("användare@exempel.se") == True
    assert validate_email("felaktig-epost") == False
```

## 2. Sökfunktion för restauranger

### Testnivå
**Rekommenderad testnivå: Integrationstest och systemtest**

*Motivering:*
- Integrationstest för att verifiera sökmotorns koppling till databasen
- Systemtest för att verifiera filtrering i verkliga scenarier

### Testmetod
**Rekommenderad testmetod: Black-box och explorativ**

*Motivering:*
- Black-box för strukturerad testning av olika sökkriterier
- Explorativ för att hitta oväntade beteenden vid kombinerad filtrering

### Enkel testkod (Python)
```python
# Integrationstest för sökning
def test_restaurant_search():
    results = search_restaurants("Stockholm", "pizza")
    assert len(results) > 0
    assert results[0]["food_type"] == "pizza"
```

## 3. Beställning

### Testnivå
**Rekommenderad testnivå: Integrationstest och systemtest**

*Motivering:*
- Integrationstest för att verifiera varukorgens koppling till betalningssystem
- Systemtest för att testa hela beställningsflödet

### Testmetod
**Rekommenderad testmetod: Black-box och explorativ**

*Motivering:*
- Black-box för att testa standardflöden för beställning
- Explorativ för att hitta användbarhetsproblem i gränssnittet

### Enkel testkod (Python)
```python
# Systemtest för beställningsflöde
def test_complete_order():
    # Lägg till vara
    add_to_cart("Pizza Margherita", 1)
    
    # Verifiera varukorg
    cart = get_cart()
    assert cart["total_amount"] == 99
    
    # Genomför betalning
    order = complete_payment("credit_card")
    assert order["status"] == "confirmed"
```

## 4. Orderhistorik

### Testnivå
**Rekommenderad testnivå: Integrationstest och acceptanstest**

*Motivering:*
- Integrationstest för att verifiera databasfrågor
- Acceptanstest för att säkerställa användarvänlig presentation

### Testmetod
**Rekommenderad testmetod: Black-box**

*Motivering:*
- Black-box för att testa användarspecifika ordervisningar och statusuppdateringar

### Enkel testkod (Python)
```python
# Integrationstest för orderhistorik
def test_order_history():
    login("test@example.com", "Password123")
    history = get_order_history()
    
    assert len(history) > 0
    assert history[0]["user_id"] == logged_in_user_id
```

## 5. Push-notiser

### Testnivå
**Rekommenderad testnivå: Integrationstest och systemtest**

*Motivering:*
- Integrationstest för att verifiera att notiser skickas vid statusändringar
- Systemtest för att verifiera leverans på olika enheter

### Testmetod
**Rekommenderad testmetod: Black-box och explorativ**

*Motivering:*
- Black-box för att testa specifika notisscenarion
- Explorativ för att testa i olika miljöer och nätverksförhållanden

### Enkel testkod (Python)
```python
# Integrationstest för push-notiser
def test_push_notification():
    # Skapa en mock-notistjänst
    mock_notification_service = MagicMock()
    
    # Ändra orderstatus
    update_order_status("order123", "on_the_way", mock_notification_service)
    
    # Verifiera att notistjänsten anropades
    mock_notification_service.send_notification.assert_called_with(
        user_id, "Din mat är på väg hem till dig"
    )
```

## Prioritering av tester baserat på risker och affärsvärde

### Högst prioritet (Kritiska tester)
1. **Beställning och betalning** - Direkt koppling till intäkter
2. **Användarregistrering och inloggning** - Grundläggande och säkerhetskritisk

### Medelhög prioritet
3. **Sökfunktion för restauranger** - Kritisk för användarupplevelsen
4. **Push-notiser** - Viktiga för användarengagemang

### Lägre prioritet
5. **Orderhistorik** - Användbar men inte kritisk för huvudflödet