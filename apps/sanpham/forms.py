
from wtforms import Form, DateField , IntegerField, StringField, BooleanField, TextAreaField, validators,DecimalField
from flask_wtf.file import FileAllowed, FileField, FileRequired
from datetime import datetime

class Addsp(Form):
    name = StringField('Tên',[validators.DataRequired()])
    price =DecimalField('Giá', [validators.DataRequired()])
    image = FileField('Ảnh', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    discription = TextAreaField('Mô tả', [validators.data_required()])