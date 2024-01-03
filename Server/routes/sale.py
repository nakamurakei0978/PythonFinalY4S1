from flask import  Blueprint, make_response,request, jsonify
from models import db, User, Product, Sale, Sale_details
import datetime
from . import secret_key, token_required

sale = Blueprint('sale', __name__)

@sale.route('/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    data = request.get_json()
    user_id = current_user.id
    sale_date = datetime.datetime.now()
    total_amount = 0
    sale_id = 0
    try:
        sale = Sale()
        sale.user_id = user_id
        sale.sale_date = sale_date
        sale.total_amount = total_amount
        db.session.add(sale)
        db.session.commit()
        sale_id = sale.id
    except:
        db.session.rollback()
        return make_response('something is wrong'), 401
    
    try:
        for i in data:
            product = Product.query.filter_by(id = i['product_id']).first()
            sale_details = Sale_details()
            qty = i['qty']
            price = product.price
            total_amount += qty * price
            
            sale_details.sale_id = sale_id
            sale_details.product_id = product.id
            sale_details.qty = qty
            sale_details.price = price
            db.session.add(sale_details)
            product.qty -= qty
        sale.total_amount = total_amount
        db.session.commit()
    except:
        db.session.rollback()   
        return make_response('something is wrong'), 401
        
    
    return make_response('success'), 200

@sale.route('/sale', methods=['GET'])
def get_sale():
    limit = request.args.get('limit')
    page = request.args.get('page')
    totalPage = 1
    if limit != 'All':
        totalPage = (Sale.query.count()/int(limit)).__ceil__()
        startAt = (int(page) * int(limit)) - int(limit)
        sales = Sale.query.join(User, Sale.user_id == User.id).add_columns(Sale.id,User.username.label('user'), Sale.sale_date, Sale.total_amount).order_by(Sale.id.desc()).limit(int(limit)).offset(startAt)
    else:
        sales = Sale.query.join(User, Sale.user_id == User.id).add_columns(Sale.id,User.username.label('user'), Sale.sale_date, Sale.total_amount).order_by(Sale.id.desc()).all()
    sale_lists = []
    for sale in sales:
        sale_details = Sale_details.query.filter_by(sale_id = sale.id).join(Product, Sale_details.product_id == Product.id).add_columns(Sale_details.id, Product.name.label('product_name'), Sale_details.qty, Sale_details.price).all()
        details = []
        for detail in sale_details:
            details.append({
                "product_name": detail.product_name,
                "qty": detail.qty,
                "price":detail.price
            })
        sale_lists.append({
            "id": sale.id,
            "user": sale.user,
            "date": sale.sale_date,
            "total": sale.total_amount,
            "details": details
        })
    
    return make_response(jsonify({'message':'success', 'sales': sale_lists, 'totalPage':totalPage})), 200 
