from flask import redirect, render_template, url_for, flash, request,session,current_app
from apps import db, app, photos
from apps.sanpham.models import addsp,Category

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/addcart', methods=['POST'])
def addcart():
    try:
        sanpham_id = request.form.get('sanpham_id')
        quantity= request.form.get('quantity')
        sanpham = addsp.query.filter_by(id=sanpham_id).first()
        if sanpham_id and quantity and request.method =="POST":
            DictItems = {sanpham_id:{'name':sanpham.name,'price':float(sanpham.price),'quantity':quantity,'image':sanpham.image,}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if sanpham_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(sanpham_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
              
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/cart')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,sanpham in session['Shoppingcart'].items():
        subtotal += float(sanpham['price']) * int(sanpham['quantity'])
        grandtotal = float(subtotal)
    return render_template('sanpham/cart.html',grandtotal=grandtotal,categories=Category)


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item is updated!')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
