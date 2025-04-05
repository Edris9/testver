Feature: Hantera orderhistorik
  Som en användare
  Vill jag kunna se min orderhistorik
  För att hålla koll på mina tidigare inköp

  Scenario: Visa tom orderhistorik
    Given användaren "nyuser" har inga tidigare beställningar
    When användaren begär att se sin orderhistorik
    Then ska systemet visa att inga ordrar hittades

  Scenario: Spara en ny order
    Given systemet är redo att ta emot ordrar
    When användaren "testuser" lägger en order med följande produkter:
      | namn     | antal | pris |
      | T-shirt  | 2     | 199  |
      | Jeans    | 1     | 599  |
    And orderns totalsumma är 997 kr
    Then ska ordern sparas i systemet
    And användaren ska få en bekräftelse

  Scenario: Visa orderhistorik med en order
    Given användaren "testuser" har en tidigare beställning
    When användaren begär att se sin orderhistorik
    Then ska systemet visa orderinformationen
    And orderinformationen ska innehålla produktnamn och priser
    And orderinformationen ska visa totalsumman
    
  Scenario: Visa orderhistorik med flera ordrar
    Given användaren "multiuser" har flera tidigare beställningar
    When användaren begär att se sin orderhistorik
    Then ska systemet visa alla ordrar i kronologisk ordning
    And varje order ska ha sitt eget ordernummer