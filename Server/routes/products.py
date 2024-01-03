import hashlib
from flask import jsonify, Blueprint, request, send_from_directory 
from models import db, Product
from werkzeug.utils import secure_filename
import os
from datetime import datetime

now=datetime.now()
timestamp = int(now.timestamp())

api_products = Blueprint('api_products', __name__)

@api_products.route('/post_product', methods=['POST'])
def post_product():
    name = request.form.get('name',type=str).strip().lower()
    qty = request.form.get('qty',type=int)
    price = request.form.get('price', type=float)
    category_id= request.form.get('category_id', type=int)
    image = request.files.get('image')
    
    if name == '':
        return jsonify({'message': 'No name part in the request'}), 400
    
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product is not None:
        return jsonify({'message': 'Product with this name already exists'}), 409
    
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage\products')
    os.makedirs(storage_dir, exist_ok = True)
    
    image_name = ''
    if image is not None:
        if image.content_type.split('/')[1] not in ['png', 'jpg', 'jpeg', 'svg', 'webp', 'gif', 'jfif', 'pjpeg', 'pjp', 'avif', 'apng']:
            return jsonify({'message': 'file should be an image!'}), 422
            
        image.seek(0, os.SEEK_END)
        size = os.fstat(image.fileno()).st_size
        if size > 5000000:
            return jsonify({'message': 'image size should not exceed 5MB!'}), 422
        image.seek(0)
        image.seek(0, os.SEEK_END)
        hash = hashlib.md5(image.read()).hexdigest()
        image.seek(0)
            
        extension = image.content_type.split('/')[1]
        image_name = secure_filename(name+hash+'.'+extension)
        image.save(os.path.join(storage_dir, image_name))
    
    try:
        product = Product()
        product.name = name
        product.qty = qty
        product.price = price
        product.category_id = category_id
        product.image = image_name
        db.session.add(product)
        db.session.commit()
    except Exception as err:
        print(err)
        db.session.rollback()
        os.remove(os.path.join(storage_dir, image_name))
        return jsonify({'message': 'something wrong!'}), 409
    return jsonify({'message':'Added successfully'}), 200


@api_products.route('/get_products', methods=['GET'])
def get_products():
    limit = request.args.get('limit')
    page = request.args.get('page',default=1)
    
    if limit is not None and limit != 'All' and limit != '':
        totalPage = (Product.query.count()/int(limit)).__ceil__()
        page_offset = (int(page)*int(limit)) - int(limit)
        products = Product.query.order_by(Product.id.desc()).offset(page_offset).limit(limit)
        
        json_products = []
        for p in products:
            json_products.append({
                'id': p.id,
                'name': p.name,
                'qty': p.qty,
                'price': p.price,
                'category_id': p.category_id,
                'image': p.image                
            })
        return jsonify({ 'products': json_products, 'totalPage':totalPage, 'message': 'success'}), 200
    
    
    totalPage = 1
    products = Product.query.order_by(Product.id.desc()).all()
        
    json_products = []
    for p in products:
        json_products.append({
            'id': p.id,
            'name': p.name,
            'qty': p.qty,
            'price': p.price,
            'category_id': p.category_id,
            'image': p.image                
        })
    return jsonify({ 'products': json_products, 'totalPage':totalPage,'message': 'success'}), 200

@api_products.route('/search_products', methods=['GET'])
def search_products():
    limit = request.args.get('limit')
    page = request.args.get('page',default=1)
    searchName = request.args.get('searchName', default='')
    print(searchName)
    if limit is not None and limit != 'All' and limit != '':
        totalPage = (Product.query.filter(Product.name.like(f'{searchName}%')).count()/int(limit)).__ceil__()
        page_offset = (int(page)*int(limit)) - int(limit)
        products = Product.query.filter(Product.name.like(f'{searchName}%')).order_by(Product.id.desc()).offset(page_offset).limit(limit)
        
        json_products = []
        for p in products:
            json_products.append({
                'id': p.id,
                'name': p.name,
                'qty': p.qty,
                'price': p.price,
                'category_id': p.category_id,
                'image': p.image                
            })
        return jsonify({ 'products': json_products, 'totalPage':totalPage,'message': 'success'}), 200
    
    
    totalPage = 1
    products = Product.query.filter(Product.name.like(f'{searchName}%')).order_by(Product.id.desc())
        
    json_products = []
    for p in products:
        json_products.append({
            'id': p.id,
            'name': p.name,
            'qty': p.qty,
            'price': p.price,
            'category_id': p.category_id,
            'image': p.image                
        })
    return jsonify({ 'products': json_products, 'totalPage':totalPage,'message': 'success'}), 200


@api_products.route('/put_product', methods=['PUT'])
def put_product():
    id = request.form.get('id', type=int)
    name = request.form.get('name', type=str).strip().lower()
    qty = request.form.get('qty', type=int)
    price = request.form.get('price', type=float)
    category_id = request.form.get('category_id',type=int)
    image = request.files.get('image')

    product = Product.query.get_or_404(id)
    if name == '':
        return jsonify({'message': 'No name part in the request'}), 400

    existing_product = Product.query.filter(Product.id != id, Product.name == name).first()
    if existing_product is not None:
        return jsonify({'message': 'Product with this name already exists'}), 409

    # storage for image
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage/products')
    os.makedirs(storage_dir, exist_ok=True)

    filename = ''
    if image is not None:
        if image.content_type.split('/')[1] not in ['png', 'jpg', 'jpeg', 'svg', 'webp', 'gif', 'jfif', 'pjpeg', 'pjp', 'avif', 'apng']:
            return jsonify({'message': 'file should be an image!'}), 422

        image.seek(0, os.SEEK_END)
        size = os.fstat(image.fileno()).st_size
        if size > 5000000:
            return jsonify({'message': 'image size should not exceed 5MB!'}), 422
        image.seek(0)
        image.seek(0, os.SEEK_END)
        hash = hashlib.md5(image.read()).hexdigest()
        image.seek(0)
    
        extension = image.content_type.split('/')[1]
        filename = secure_filename(name+hash+'.'+extension)
        old_imagePath = os.path.join(storage_dir, product.image)
        if os.path.isfile(old_imagePath):
            os.remove(old_imagePath)
        image.save(os.path.join(storage_dir, filename))
    
    else:
        if product.image != '':
            extension = product.image.split('.')[1]
            filename = secure_filename(name+'.'+extension)
            new_imagePath = os.path.join(storage_dir, filename)
            old_imagePath = os.path.join(storage_dir, product.image)
            if os.path.isfile(old_imagePath):
                os.rename(old_imagePath, new_imagePath)

    try:
        product.name = name
        product.qty = qty
        product.price = price
        product.category_id = category_id
        product.image = filename
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'something wrong!'}), 409

    updated_product_dict = {
        'id': product.id,
        'name': product.name,
        'qty': product.qty,
        'price': product.price,
        'category_id': product.category_id,
        'image': product.image
    }

    return jsonify({'message': 'updated successfully!', 'product': updated_product_dict}), 200


@api_products.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    # storage for image
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage/products')


    try:
        db.session.delete(product)
        db.session.commit()
        # Check if an image file exists and delete it
        if product.image:
            image_path = os.path.join(storage_dir, product.image)
            if os.path.isfile(image_path):
                os.remove(image_path)
    except:
        db.session.rollback()
        return jsonify({'message': 'something wrong!'}), 409

    return jsonify({'message': 'deleted successfully!'}), 200



@api_products.route('/storage/products/<filename>')
def serve_image(filename):
    return send_from_directory('storage/products', filename)