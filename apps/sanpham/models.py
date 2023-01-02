from apps import db, app
from datetime import datetime


class addsp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    decs = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('categories', lazy=True))

    image = db.Column(db.String(150), nullable=False, default='image.jpg')
    def __repr__(self):
        return '<addsp %r>' % self.title
    

class Category(db.Model): #Loại hàng
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name



with app.app_context():
    db.create_all()