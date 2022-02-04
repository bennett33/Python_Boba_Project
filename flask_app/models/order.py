from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user 
from flask import flash


class Order:

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.tea = data['tea']
        self.ice = data['ice']
        self.sugar = data['sugar']
        self.topping = data['topping']
        self.another_topping = data['another_topping']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = user.User.get_by_id({"id": data["user_id"]})

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO orders (user_id, tea, ice, sugar, topping, another_topping, price, created_at, updated_at) VALUES (%(user_id)s, %(tea)s, %(ice)s, %(sugar)s, %(topping)s, %(another_topping)s, %(price)s, NOW(), NOW());"
        return connectToMySQL("boba_schema").query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL("boba_schema").query_db(query)
        orders = []
        for row in results:
            orders.append(cls(row))
        return orders


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL("boba_schema").query_db(query,data)
        return cls( results[0] )


    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['tea']) < 2:
            is_valid = False
            flash("Must choose tea")
        return is_valid


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL("boba_schema").query_db(query,data)
