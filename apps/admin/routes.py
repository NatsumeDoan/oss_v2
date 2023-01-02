from flask import render_template, session, request, redirect, url_for, flash
from apps.sanpham.models import addsp,Category
from apps import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
@app.route('/')
def admin():
    #bắt đầu minh code#
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    #kết thúc#
    sanpham = addsp.query.all()
    return render_template('admin/index.html',title="Admin Page",sanpham=sanpham)

@app.route('/categories')
def categories():
    #bắt đầu minh code#
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    #kết thúc#
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories.html', title='categories',categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,phone=form.phone.data,
                    address=form.address.data,password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering','success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data} You are logined','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again','danger')
            
    return render_template('admin/login.html', form=form, title="Login now!")

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('login'))