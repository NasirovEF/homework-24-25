import stripe
from config.settings import STRIPE_API_KEY

NULLABLE = {"null": True, "blank": True}
stripe.api_key = STRIPE_API_KEY


def get_product(product):
    return stripe.Product.create(name=product)


def get_price(amount, product):
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product.get("name")},
    )


def get_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
