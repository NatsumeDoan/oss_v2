from flask import redirect, render_template, url_for, flash, request,session,current_app
from apps import db, app, photos
from .models import Category, addsp
from .forms import Addsp
import secrets
from datetime import datetime
import os

@app.route('/home')
def home():
    sanpham = addsp.query.order_by("name").all() #select tất cả sản phẩm ở DB và sắp xếp theo ABC
    category = Category.query.join(addsp, (Category.id == addsp.category_id)).all()
    return render_template('sanpham/index.html',sanpham=sanpham, category=category)

@app.route('/category/<int:id>')
def get_category(id):
    cate = addsp.query.filter_by(category_id=id)
    category = Category.query.join(addsp, (Category.id == addsp.category_id)).all()

    return render_template('sanpham/index.html',catalog=cate, category=category)


@app.route('/addCate', methods=['GET', 'POST'])
def addCate(): #Thêm loại
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getcate = request.form.get('cate')
        cate = Category(name=getcate)
        db.session.add(cate)
        flash(f'Loại {getcate} đã được thêm vào database', 'success')
        db.session.commit()
        return redirect(url_for('addCate'))
    return render_template('sanpham/addCate.html')

@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('sanpham/updatecat.html', title='cập nhập loại',updatecat=updatecat)

@app.route('/deletecat/<int:id>',methods=['POST'])
def deletecat(id):
    deletecat= Category.query.get_or_404(id)
    db.session.query(addsp).filter(addsp.category_id==id).delete()
    if request.method=="POST":
        db.session.delete(deletecat)
        db.session.commit()
        flash(f'The category {deletecat.name} was delete from your database','success')
        return redirect(url_for('admin'))
    flash(f'The category {deletecat.name} cant be delete','fail')
    return redirect(url_for('admin'))

@app.route('/addSp', methods=['GET', 'POST'])
def addSp():
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    form = Addsp(request.form)
    categories = Category.query.all()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        decs = form.discription.data
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+ ".")
        date = datetime.now()
        category = request.form.get('category')
        
        addSanpham = addsp(name=name,price=price,decs = decs, pub_date=date, 
        category_id= category ,image=image)
        db.session.add(addSanpham)
        flash(f'{name} đã được thêm vào database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('sanpham/addsp.html', form=form, title="Thêm sản phẩm", categories=categories)
@app.route('/deletesp/<int:id>',methods=['POST'])
def deletesp(id):
    deletesp= addsp.query.get_or_404(id)
    if request.method=="POST":
        try :
            os.unlink(os.path.join(current_app.root_path,"static/images/"+deletesp.image))
        except Exception as e:
            print(e)
        db.session.delete(deletesp)
        db.session.commit()
        flash(f'The category {deletesp.name} was delete from your database','success')
        return redirect(url_for('admin'))
    flash(f'The category {deletesp.name} cant be delete','fail')
    return redirect(url_for('admin'))

@app.route('/updateSp/<int:id>', methods=['GET', 'POST'])
def updateSp(id):
    categories = Category.query.all()
    sp = addsp.query.get_or_404(id)
    form = Addsp(request.form)
    category = request.form.get('category')
    if request.method == "POST":
        sp.name = form.name.data
        sp.price = form.price.data
        sp.decs = form.discription.data
        sp.category_id = category
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + sp.image)) #xoá ảnh khỏi thư mục images
                sp.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+ ".") #tải lên hình ảnh mới
            except:
                sp.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+ ".") #tải ảnh mới lên

        db.session.commit()
        flash(f'Sản phẩm đã được cập nhật', 'success')
        return redirect(url_for('admin'))
    form.name.data = sp.name
    form.price.data = sp.price
    form.discription.data = sp.decs
    return render_template('sanpham/updatesp.html', form=form, categories=categories, sanpham=sp)

@app.route('/chitiet/<int:id>')
def chitiet(id):
    sanpham = addsp.query.get_or_404(id)
    category = Category.query.join(addsp, (Category.id == addsp.category_id)).all()
    return render_template('sanpham/chitiet.html', sanpham=sanpham,category=category)
