from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    name = StringField('Họ và tên', [validators.Length(min=4, max=35)])
    username = StringField('Tài khoản', [validators.Length(min=4, max=25)])
    phone = StringField('Số điện thoại', [validators.Length(10)])
    address = StringField('Địa chỉ', [validators.Length(min=6, max=50)])
    password = PasswordField('Mật khẩu mới', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Mật khẩu không khớp')
    ])
    confirm = PasswordField('Nhập lại mật khẩu')

class LoginForm(Form):
     username = StringField('Tài khoản', [validators.Length(min=4, max=25)])
     password = PasswordField('Mật khẩu', [validators.DataRequired() ])