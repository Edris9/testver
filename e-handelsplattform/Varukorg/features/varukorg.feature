# features/varukorg.feature

Feature: Hantera Varukorg
  Som en användare vill jag kunna hantera min varukorg
  så att jag kan lägga till, ändra och ta bort produkter
  och se det totala priset.

  Scenario: Lägga till en produkt i en tom varukorg
    Given att jag har en tom varukorg
    When jag lägger till 1 "Blå T-shirt" i varukorgen
    Then ska min varukorg innehålla 1 "Blå T-shirt"

  Scenario: Lägga till samma produkt igen
    Given att jag har 2 "Blå T-shirt" i varukorgen
    When jag lägger till ytterligare 1 "Blå T-shirt" i varukorgen
    Then ska min varukorg innehålla 3 "Blå T-shirt"

  Scenario: Lägga till flera olika produkter
    Given att jag har en tom varukorg
    When jag lägger till 1 "Blå T-shirt" i varukorgen
    And jag lägger till 1 "Svarta Jeans" i varukorgen
    Then ska min varukorg innehålla 1 "Blå T-shirt" och 1 "Svarta Jeans"

  Scenario: Ta bort en produkt från varukorgen
    Given att jag har 1 "Blå T-shirt" i varukorgen
    When jag tar bort 1 "Blå T-shirt" från varukorgen
    Then ska min varukorg vara tom

  Scenario: Ta bort en del av antalet av en produkt
    Given att jag har 3 "Blå T-shirt" i varukorgen
    When jag tar bort 1 "Blå T-shirt" från varukorgen
    Then ska min varukorg innehålla 2 "Blå T-shirt"

  Scenario: Försöka ta bort mer än vad som finns
    Given att jag har 1 "Blå T-shirt" i varukorgen
    When jag försöker ta bort 2 "Blå T-shirt" från varukorgen
    Then ska min varukorg vara tom

  Scenario: Beräkna totalpriset för flera produkter
    Given att jag har 2 "Blå T-shirt" i varukorgen
    And jag har 1 "Svarta Jeans" i varukorgen
    When jag beräknar totalpriset
    Then ska totalpriset vara 1100 kr

  Scenario: Uppdatera antalet av en produkt
    Given att jag har 1 "Blå T-shirt" i varukorgen
    When jag ändrar antalet av "Blå T-shirt" till 3
    Then ska min varukorg innehålla 3 "Blå T-shirt"

  Scenario: Rensa hela varukorgen
    Given att jag har 2 "Blå T-shirt" och 1 "Svarta Jeans" i varukorgen
    When jag rensar varukorgen
    Then ska min varukorg vara tom

  Scenario: Försöka lägga till en produkt som inte finns i katalogen
    Given att jag har en tom varukorg
    When jag försöker lägga till 1 "Okänd Produkt" med ID 3 i varukorgen
    Then ska produkten inte läggas till i varukorgen
    And ett meddelande visas att produkten inte hittades

  Scenario: Försöka lägga till fler produkter än vad som finns i lager
    Given att produkten "Blå T-shirt" har 5 enheter i lager
    And jag har en tom varukorg
    When jag försöker lägga till 6 "Blå T-shirt" i varukorgen
    Then ska produkten inte läggas till i varukorgen
    And ett meddelande visas att lagret är otillräckligt