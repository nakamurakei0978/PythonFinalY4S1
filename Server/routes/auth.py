from flask import  Blueprint, request, make_response, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User
from jwt import encode, decode
import datetime
from functools import wraps
import uuid


auth = Blueprint('auth', __name__)

secret_key = 'thisisthesecretkey'

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = decode(token, secret_key, algorithms = ['HS256'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        user = User.query.filter_by(username=data['user']).first()
        if not user or user.is_active != 1 or user.role != 'admin':
            return jsonify({'message': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        
        try:
            data = decode(token, secret_key, algorithms = ['HS256'])
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(current_user,*args, **kwargs)
    return decorated
    
    
@auth.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this'})
@auth.route('/protected')    
@token_required
def protected():
    return jsonify({'message':'Only for valid Token'})

@auth.route('/verify-admin')
@token_required
def isAdmin(current_user):
    if current_user.admin:
        return jsonify({'message':'true'})
    return jsonify({'message':'false'})
@auth.route('/verify-login')
@token_required
def isLoggedIn(current_user):
    if current_user:
        return jsonify({'message': 'true'})
    return jsonify({'message': 'false'})

    
@auth.route('/login')
def user_login():
    auth = request.authorization
    
    if  auth and auth.username and auth.password:
        existingUser = User.query.filter_by(username = auth.username).first()
        if existingUser and check_password_hash(existingUser.password, auth.password):
            token = encode({'public_id':existingUser.public_id, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(days=3)}, secret_key)
            return jsonify({'token':token ,'message' : 'Login successfully'}), 200
        
    return make_response('Could not verify!',401, {'WWW-Authentication':'Basic-realm="Login required!"'})
    
@auth.route('/register', methods=['POST'])
def user_register():
    data = request.get_json()
    
    if data and data.get('username') and data.get('password'):
        existingUser = User.query.filter_by(username = data.get('username')).first()
        if existingUser:
            return make_response('User already exists!', 400)
        hashed_password = generate_password_hash(data.get('password'))
        new_user = User(username = data.get('username'), password = hashed_password, active = True, public_id = str(uuid.uuid4()), admin = False)
        try:   
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'message': 'New user created!'}), 201)
        except:
            db.session.rollback()
            make_response(jsonify({'message': 'Something is wrong'}), 401)
    return make_response('Could not verify!', 400, {'WWW-Authentication': 'Basic realm="Register required!"'})

