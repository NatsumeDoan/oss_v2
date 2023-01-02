from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os 


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'saleapp.db')
app.config['SECRET_KEY']= os.environ.get('SECRET_KEY') or 'your-hard-secret-key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from apps.admin import routes
from apps.sanpham import routes
from apps.cart import cart
from apps.khachhang import routes