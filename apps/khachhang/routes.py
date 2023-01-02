from flask import render_template, session, request, redirect, url_for, flash
from apps import app, db, bcrypt
from .forms import dangkykhachhang,dangnhapkhachhang
from .models import Khachhang

@app.route('/dangky', methods=['GET', 'POST'])
def dangky():
    form = dangkykhachhang(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.matkhau.data)
        khachhang = Khachhang(name=form.name.data,taikhoan=form.taikhoan.data,phone=form.phone.data,
                    address=form.address.data,matkhau=hash_password)
        db.session.add(khachhang)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering','success')
        return redirect(url_for('dangky'))
    return render_template('khachhang/dangky.html', form=form)

@app.route('/dangnhap', methods=['GET', 'POST'])
def dangnhap():
    form = dangnhapkhachhang(request.form)
    if request.method == "POST" and form.validate():
        khachhang = Khachhang.query.filter_by(taikhoan = form.taikhoan.data).first()
        if khachhang and bcrypt.check_password_hash(khachhang.matkhau, form.matkhau.data):
            session['taikhoan'] = form.taikhoan.data
            flash(f'Welcome {form.taikhoan.data} You are logined','success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Wrong Password please try again','danger')
            
    return render_template('khachhang/dangnhap.html', form=form, title="Login now!")

@app.route('/dangxuat')
def dangxuat():
    session.pop('taikhoan')
    return redirect(url_for('dangnhap'))

