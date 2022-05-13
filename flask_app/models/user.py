from sqlite3 import connect
from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument




EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = 'login_and_registration_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"

        user = connectToMySQL(cls.db).query_db(query, data)

        return user

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)

        user = cls(result[0])
        return user

    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == ():
            return False
        
        user = cls(result[0])

        return user


# +++++++++++++++++++++++++++++++
# Static methods below

    @staticmethod
    def validate_user_registration(user):
        is_valid = True

        if not user['first_name'].isalpha():
            flash('Name must contain only letters', 'reg')
            is_valid = False
        if not len(user['first_name']) > 2:
            flash('First name must be longer than 2 characters', 'reg')
            is_valid = False
        if not user['last_name'].isalpha():
            flash('Last name must contain only letters', 'reg')
            is_valid = False
        if not len(user['last_name']) > 2:
            flash('Last name must be longer than 2 characters', 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", 'reg')
            is_valid = False
        if not len(user['password']) > 7:
            flash('Password must be at least 8 characters', 'reg')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Passwords do not match', 'reg')
            is_valid = False
        return is_valid
