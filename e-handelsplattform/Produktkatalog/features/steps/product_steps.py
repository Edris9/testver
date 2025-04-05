from behave import given, when, then
from product_Catalo import Product, ProductCatalog

@given('that the following products exist in the catalog')
def step_impl(context):
    context.catalog = ProductCatalog()
    for row in context.table:
        product = Product(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            price=float(row['price']),
            category=row['category'],
            in_stock=int(row['in_stock'])
        )
        context.catalog.add_product(product)

@when('I search for "{keyword}"')
def step_impl(context, keyword):
    context.search_results = context.catalog.search(keyword)

@when('I browse the category "{category}"')
def step_impl(context, category):
    context.search_results = context.catalog.get_products_by_category(category)

@when('I view details for product with id "{product_id}"')
def step_impl(context, product_id):
    context.product = context.catalog.get_product(product_id)

# Lägg till specifika steg för singular och plural för att matcha feature-filen exakt
@then('I should see 1 product in the result')
def step_impl(context):
    assert len(context.search_results) == 1, \
        f"Expected 1 product, but got {len(context.search_results)}"

@then('I should see 0 products in the result')
def step_impl(context):
    assert len(context.search_results) == 0, \
        f"Expected 0 products, but got {len(context.search_results)}"

@then('I should see 2 products in the result')
def step_impl(context):
    assert len(context.search_results) == 2, \
        f"Expected 2 products, but got {len(context.search_results)}"

# Behåll den generiska versionen för framtida användning
@then('I should see {count:d} product(s) in the result')
def step_impl(context, count):
    assert len(context.search_results) == count, \
        f"Expected {count} products, but got {len(context.search_results)}"

@then('the result should contain product with id "{product_id}"')
def step_impl(context, product_id):
    found = any(p.id == product_id for p in context.search_results)
    assert found, f"Product with id {product_id} not found in the result"

@then('I should see the product name "{name}"')
def step_impl(context, name):
    assert context.product.name == name, \
        f"Expected product name {name}, but got {context.product.name}"

@then('I should see the product price {price:d}')
def step_impl(context, price):
    assert context.product.price == price, \
        f"Expected price {price}, but got {context.product.price}"

@then('I should see that there are {count:d} in stock')
def step_impl(context, count):
    assert context.product.in_stock == count, \
        f"Expected {count} in stock, but got {context.product.in_stock}"

@then('the result should be empty')
def step_impl(context):
    assert len(context.search_results) == 0, \
        "Expected empty result, but got results."

@then('the product description should be "{description}"')
def step_impl(context, description):
    assert context.product.description == description, \
        f"Expected description '{description}', but got '{context.product.description}'"

@then('the product category should be "{category}"')
def step_impl(context, category):
    assert context.product.category == category, \
        f"Expected category '{category}', but got '{context.product.category}'"