import hashlib
from flask import jsonify, Blueprint, request, send_from_directory 
from models import db, Category
from werkzeug.utils import secure_filename
import os


api_categories = Blueprint('api_categories', __name__)


@api_categories.route('/post_category', methods=['POST'])
def post_category():
    name = request.form.get('name').strip().lower()
    image = request.files.get('image')
    
    if name == '':
        return jsonify({'message': 'No name part in the request'}), 400
    
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category is not None:
        return jsonify({'message': 'Category with this name already exists'}), 409
    
    #storage for image
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage/categories')
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
        image.save(os.path.join(storage_dir, filename))
        
    
    try:
        category = Category()
        category.name = name
        category.image = filename
        db.session.add(category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'something wrong!'}), 409
    
    new_category = Category.query.order_by(Category.id.desc()).first()
    new_category_dict = {
        'id': new_category.id,
        'name': new_category.name,
        'image': new_category.image
    }
    
    
    return jsonify({'message': 'added successfully!','category': new_category_dict}), 201


@api_categories.route('/get_categories', methods=['GET'])
def get_categories():
    limit = request.args.get('limit')
    page = request.args.get('page')
    if limit is not None:
        totalPage = (Category.query.count()/int(limit)).__ceil__()   
        startAt = (int(page) * int(limit)) - int(limit)
        
        categories = Category.query.order_by(Category.id.desc()).offset(startAt).limit(limit)
        json_string = []
        for c in categories:
            json_string.append({
                'id': c.id,
                'name': c.name,
                'image': c.image,
            })
        return jsonify({'categories':json_string, 'totalPage':totalPage, 'message': 'success'}), 200
    
    categories = Category.query.order_by(Category.id.desc()).all()
    json_string = []
    for c in categories:
        json_string.append({
            'id': c.id,
            'name': c.name,
            'image': c.image,
        })
    return jsonify({'categories':json_string, 'totalPage':1, 'message': 'success'}), 200


@api_categories.route('/put_category/<int:id>', methods=['PUT'])
def put_category(id):
    category = Category.query.get_or_404(id)

    name = request.form.get('name').strip().lower()
    image = request.files.get('image')
    if name == '':
        return jsonify({'message': 'No name part in the request'}), 400

    existing_category = Category.query.filter(Category.id != id, Category.name == name).first()
    if existing_category is not None:
        return jsonify({'message': 'Category with this name already exists'}), 409

    # storage for image
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage/categories')
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
        old_imagePath = os.path.join(storage_dir, category.image)
        if os.path.isfile(old_imagePath):
            os.remove(old_imagePath)
        image.save(os.path.join(storage_dir, filename))
    
    else:
        if category.image != '':
            extension = category.image.split('.')[1]
            filename = secure_filename(name+'.'+extension)
            new_imagePath = os.path.join(storage_dir, filename)
            old_imagePath = os.path.join(storage_dir, category.image)
            if os.path.isfile(old_imagePath):
                os.rename(old_imagePath, new_imagePath)

    try:
        category.name = name
        category.image = filename
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'something wrong!'}), 409

    updated_category_dict = {
        'id': category.id,
        'name': category.name,
        'image': category.image
    }

    return jsonify({'message': 'updated successfully!', 'category': updated_category_dict}), 200


@api_categories.route('/delete_category/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)

    # storage for image
    project_dir = os.getcwd()
    storage_dir = os.path.join(project_dir, 'storage/categories')


    try:
        db.session.delete(category)
        db.session.commit()
        # Check if an image file exists and delete it
        if category.image:
            image_path = os.path.join(storage_dir, category.image)
            if os.path.isfile(image_path):
                os.remove(image_path)
    except:
        db.session.rollback()
        return jsonify({'message': 'something wrong!'}), 409

    return jsonify({'message': 'deleted successfully!'}), 200


@api_categories.route('/storage/categories/<filename>')
def serve_image(filename):
    return send_from_directory('storage/categories', filename)


@api_categories.route('/search_categories')
def search_category():
    search = request.args.get('search','')
    limit = request.args.get('limit')
    page = request.args.get('page', 1)
    total_page = 1
    if limit is not None and limit != 'All':
        startAt = (int(page) * int(limit)) - int(limit)
        categories = Category.query.filter(Category.name.like(f'{search}%')).order_by(Category.id.desc()).offset(startAt).limit(limit)
        
        total_categories = Category.query.filter(Category.name.like(f'{search}%')).order_by(Category.id.desc()).count()
        print(total_categories)
        total_page = (total_categories/int(limit)).__ceil__()
    else:
        categories = Category.query.filter(Category.name.like(f'{search}%')).order_by(Category.id.desc())
    
    json_string = []
    for c in categories:
        json_string.append({
            'id': c.id,
            'name': c.name,
            'image': c.image,
        })
    
    
    return jsonify({'categories':json_string, 'totalPage': total_page}), 200