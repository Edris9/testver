
Feature: Användarhantering i inloggningssystemet
  Som en användare
  Vill jag kunna registrera mig och logga in
  För att komma åt mitt konto

  Scenario: Registrera en ny användare
    Given systemet är igång
    When användaren väljer att registrera sig
    And anger användarnamn "testuser"
    And anger lösenord "password123" 
    Then ska användaren bli registrerad
    And systemet ska visa "har registrerats"

  Scenario: Logga in med korrekta uppgifter
    Given en användare med namn "testuser" och lösenord "password123" finns
    When användaren väljer att logga in
    And anger användarnamn "testuser"
    And anger lösenord "password123"
    Then ska användaren bli inloggad
    And systemet ska visa "Inloggad som"

  Scenario: Logga in med felaktiga uppgifter
    Given en användare med namn "testuser" och lösenord "password123" finns
    When användaren väljer att logga in
    And anger användarnamn "testuser"
    And anger lösenord "fel_lösenord"
    Then ska användaren inte bli inloggad
    And systemet ska visa "Felaktigt användarnamn eller lösenord"