from wtforms import Form, BooleanField, StringField, PasswordField, validators,ValidationError
from .models import Khachhang

class dangkykhachhang(Form):
    name = StringField('Họ và tên', [validators.Length(min=4, max=35)])
    taikhoan = StringField('Tài khoản', [validators.Length(min=4, max=25)])
    phone = StringField('Số điện thoại', [validators.Length(10)])
    address = StringField('Địa chỉ', [validators.Length(min=6, max=50)])
    matkhau = PasswordField('Mật khẩu mới', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Mật khẩu không khớp')
    ])
    confirm = PasswordField('Nhập lại mật khẩu')
    def validate_username(self, username):
        if Khachhang.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")


class dangnhapkhachhang(Form):
    taikhoan = StringField('Tài khoản', [validators.Length(min=4, max=25)])
    matkhau = PasswordField('Mật khẩu', [validators.DataRequired() ])