from flask import Blueprint, request, jsonify
import os
import stripe
from models import db, Product, Category

stripe_payment = Blueprint('stripe_payment', __name__)

stripe_key = os.environ.get('STRIPE_PRIVATE_KEY')
stripe.api_key = stripe_key
storeItems = {
    1: {'priceInCents': 10000, 'name': 'Learn vue'},
    2: {'priceInCents': 20000, 'name': 'learn stripe'},
}

@stripe_payment.route('/stripe_payment', methods=['POST'])
def payment():
    try:
        items = request.json['items']
        line_items = []
        for item in items:
            product = Product.query.filter_by(id = int(item['id'])).join(Category).add_columns(Product.name, Product.price, Category.name.label('category_name')).first()
            print(product.category_name)
            store_item = storeItems.get(item['id'])
            line_item = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                        'description': product.category_name
                    },
                    'unit_amount': int(product.price*10),
                },
                'quantity': item['qty'],
            }
            line_items.append(line_item)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=line_items,
            success_url=os.environ['CLIENT_URL'] + '/product',
            cancel_url=os.environ['CLIENT_URL'] + '/product',
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500