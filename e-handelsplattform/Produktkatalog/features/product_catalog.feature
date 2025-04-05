Feature: product catalog
    To be able to shop for products
    As a customer
    I want to be able to search and browse products

    Background:
        Given that the following products exist in the catalog:
            | id | name      | description       | price | category  | in_stock |
            | 1  | T-shirt   | A white t-shirt   | 199   | Clothes   | 10       |
            | 2  | Jeans     | Blue jeans        | 499   | Clothes   | 5        |
            | 3  | Sneakers  | White sneakers    | 899   | Shoes     | 3        |

    Scenario: Search for a product by name
        When I search for "T-shirt"
        Then I should see 1 product in the result
        And the result should contain product with id "1"

    Scenario: Search for a product that does not exist
        When I search for "Hat"
        Then I should see 0 products in the result

    Scenario: Browse a product category
        When I browse the category "Clothes"
        Then I should see 2 products in the result
        And the result should contain product with id "1"
        And the result should contain product with id "2"

    Scenario: View details for a product
        When I view details for product with id "3"
        Then I should see the product name "Sneakers"
        And I should see the product price 899
        And I should see that there are 3 in stock