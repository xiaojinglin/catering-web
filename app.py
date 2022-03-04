from models import db, Customer, Order, Dish, app
from flask import Flask, render_template, session, url_for, request, redirect


@app.route('/')
def index():
    if not Customer.query.filter_by(name='new customer').count():
        new_customer = Customer(name='new customer', phone='1111111111')
        db.session.add(new_customer)
        db.session.commit()
    dishes = Dish.query.all()
    return render_template('index.html', dishes=dishes)


@app.route('/add-order/<id>', methods=['GET', 'POST'])
def add_order(id):
    if request.form:  
        if request.form["summit_order"] == "Summit":
            dish = Dish.query.get(id)
            customer = Customer.query.filter_by(name='new customer').first()
            order = Order.query.filter_by(name=dish.name).filter_by(customer_id=customer.id).first()
            if order:
                order.qty += int(request.form['qty'])
            else:
                new_order = Order(name=dish.name, price=dish.price,
                            qty=int(request.form['qty']),customer_id=customer.id)
                db.session.add(new_order)       
            db.session.commit()
        return redirect(url_for('index'))


@app.route('/dish/<id>')
def dish(id):
    dish = Dish.query.get(id)
    return render_template('dish.html', dish=dish)


@app.route('/check_out')
def check_out():
    customer=Customer.query.filter_by(name='new customer').first()
    orders = customer.orders
    total = 0
    if orders:     
        for order in orders:
            total += order.price/100 *order.qty
        return render_template('check_out.html', orders=orders, total=total)
    return redirect(url_for('index'))


@app.route('/finish',methods=['GET', 'POST'])
def finish():
     if request.form:
        new_customer = Customer.query.filter_by(name='new customer').first()
        new_customer.name = request.form['name']
        new_customer.phone = request.form['phone']
        db.session.commit()
        return render_template('finish.html')
     return redirect(url_for('index'))


@app.route('/show-order')
def show_order():
    new_customer = Customer.query.filter_by(name='new customer').first()
    return render_template('editorder.html', orders=new_customer.orders)


@app.route('/edit-order/<id>', methods=['GET', 'POST'])
def edit_order(id):
    new_customer = Customer.query.filter_by(name='new customer').first()
    order = Order.query.get(id)
    if request.form:
        if request.form['edit_del']=='Edit':
            order.qty = request.form['qty']           
        else:
            db.session.delete(order)
        db.session.commit()
    if not order:
        return redirect(url_for('index'))
    return render_template('editorder.html', orders = new_customer.orders)


if __name__ == '__main__':
    db.create_all()
    dishes=[
            Dish(url='/static/img/beef.jpg',alt='beef',name='Beef Stew',
                 ingredients='beef,potato,carrot,onion,red wine,tomatoes',price=1099),
            Dish(url='/static/img/chicken.jpg',alt='chicken',name='Curry Chicken',
                 ingredients='chicken,potato,carrot,onion,curry powder,tomatoes',price=899),
            Dish(url='/static/img/salmon.jpg',alt='salmon',name='Grilled Salmon',
                 ingredients='salmon, olive oil,vegetable salad',price=1299),
            Dish(url='/static/img/bean.jpg',alt='bean',name='Black Bean Soup',
                 ingredients='black bean, tomatoes, onion, galic',price=699)
            ]
    for dish in dishes:
        if not Dish.query.filter_by(name=dish.name).count():
            db.session.add(dish)
    db.session.commit()
    app.run(debug=True, port=8000, host='0.0.0.0')