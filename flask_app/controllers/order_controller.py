from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order


@app.route('/orders/new')
def new_band():
    if 'uuid' not in session:
        return redirect('/registration')
    data = {
        "id":session['uuid']
    }
    return render_template('order.html')


@app.route("/orders/create", methods = ['POST'])
def create_order():
    if 'uuid' not in session:
        return redirect('/logout')
    if not Order.validate_order(request.form):
        return redirect('/orders/cart')
    items = {
        'Sun Moon Lake Black Tea': 560,
        'Honey Mountain Tea': 580,
        'Songboling Mountain Tea': 580,
        'Fruit Tea': 420,
        'Passion Fruit Green Tea': 480,
        'Pineapple Green Tea': 480,
        'Green Plum Green Tea': 480,
        'Black Tea Latte': 440,
        'Green Tea Latte': 440,
        'Oolong Tea Latte': 440,
        'Winter Melon Latte': 580,
        '100% Ice': 0,
        '75% Ice': 0,
        '50% Ice': 0,
        '25% Ice': 0,
        'No Ice': 0,
        '100% Sugar': 0,
        '75% Sugar': 0,
        '50% Sugar': 0,
        '25% Sugar': 0,
        'No Sugar': 0,
        'Salted Cream': 50,
        'Cheese Foam': 50,
        'Black Sugar Pearl': 50,
        'Aiyu Jelly': 50,
        'None': 0
    } 
    data = {
        "tea": request.form["tea"],
        "ice": request.form["ice"],
        "sugar": request.form["sugar"],
        "topping": request.form["topping"],
        "another_topping": request.form["another_topping"],
        "price": items[request.form["tea"]] + items[request.form["ice"]] + items[request.form["sugar"]] + items[request.form["topping"]] + items[request.form["another_topping"]],
        "user_id": session["uuid"]
    }
    Order.create(data)
    return redirect('/orders/cart')


@app.route("/orders/cart")
def cart():
    if 'uuid' not in session:
        return redirect('/')
    data ={
        'id': session['uuid']
    }
    order=User.get_users_with_orders(data)
    # test=order.orders[0]
    # print(test.tea)
    return render_template("cart.html", order=order)



@app.route('/orders/destroy/<int:id>')
def destroy_order(id):
    if 'uuid' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Order.destroy(data)
    return redirect('/orders/cart')


@app.route("/orders/buy")
def byebye():
    if 'uuid' not in session:
        return redirect('/')
    data ={
        'id': session['uuid']
    }
    order=User.get_users_with_orders(data)
    return render_template("buy.html", order=order)