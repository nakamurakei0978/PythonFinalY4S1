from routes.categories import api_categories
from routes.products import api_products
from routes.stripe import stripe_payment
from routes.auth import auth, secret_key, token_required
from routes.sale import sale