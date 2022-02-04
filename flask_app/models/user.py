from flask import flash
from flask_bcrypt import Bcrypt
import re


from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import order
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    schema = "boba_schema" 
    # set schema name here

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.orders = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.schema).query_db(query,data)


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])


    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """

        return connectToMySQL(cls.schema).query_db(query, data)

    
    @classmethod
    def get_users_with_orders(cls, data):
        query = "SELECT * FROM users LEFT JOIN orders ON users.id = orders.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        this_user = cls(results[0])

        print(results)
        if results[0]["orders.id"] != None:
            for row_data in results:
                print(row_data)
                order_data = {
                    "id": row_data["orders.id"],
                    "tea": row_data["tea"],
                    "ice": row_data["ice"],
                    "sugar": row_data["sugar"],
                    "topping": row_data["topping"],
                    "another_topping": row_data["another_topping"],
                    "price": row_data["price"],
                    "created_at": row_data["orders.created_at"],
                    "updated_at": row_data["orders.updated_at"],
                    "user_id": row_data["user_id"]
                }
                this_user.orders.append(order.Order(order_data))
        return this_user


    @staticmethod
    def register_validator(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.schema).query_db(query,user)
        # (User.db) User is the class name!!
        if results:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
        return is_valid

    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash("Invalid Credentials")
            return False

        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("Invalid Credentials")
            return False

        return True