from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.order import Order
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registration")
def registration():
    if "uuid" in session:
        return redirect("/")
    return render_template("register.html")




@app.route('/register',methods=['POST'])
def register():

    if not User.register_validator(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['uuid'] = id
    # ['user_id'] user_id just a var you make , make sure to use the same var name 
    return redirect('/orders/new')







@app.route("/login", methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']})
    session['uuid'] = user.id
    return redirect("/orders/new")



@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")