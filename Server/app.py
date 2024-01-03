from flask import Flask
from flask_cors import CORS
from models import db
from routes import api_categories, api_products, stripe_payment, auth, sale

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/api_python'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all() 


# app.config['UPLOAD_FOLDER'] = 'storage/categories'
app.register_blueprint(api_categories)
app.register_blueprint(api_products)
app.register_blueprint(stripe_payment)
app.register_blueprint(auth)
app.register_blueprint(sale)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)