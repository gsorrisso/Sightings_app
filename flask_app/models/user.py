from flask_app.config.mysqlconnection import connectToMySQL
#in the class apps you need this ^ written from folder to file 
from flask import flash, request
from flask_app import bcrypt
import re	# the regex module

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 




class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def get_email(cls, data):

        query = "SELECT * FROM sasquatch.users WHERE email = %(email)s;"

        result = connectToMySQL('sasquatch').query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def get_id(cls, data):

        query = "SELECT * FROM sasquatch.users WHERE id = %(id)s;"

        results = connectToMySQL('sasquatch').query_db(query, data)
        return cls(results[0]) if results else None

    @staticmethod
    def validate_registration(user_information):
        is_valid = True
        data = {
            'email': request.form['email']
        }
        if len(user_information['first_name']) <= 0:
            flash('First name required!', 'register')
            is_valid = False

        if len(user_information['last_name']) <= 0:
            flash('Last name required!', 'register')
            is_valid = False

        if len(user_information['email']) <= 0:
            flash('Email required!', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user_information['email']):
            flash('Invalid Email Address', 'register')
            is_valid = False

        if len(user_information['password']) <= 5:
            flash('Password must be at least 5 characters', 'register')
            is_valid = False

        if user_information['password'] != user_information['confirm_password']:
            flash('Passwords need to match', 'register')
            is_valid = False        
        
        if not EMAIL_REGEX.match(user_information['email']):
            flash('Invalid credentials','login')
            return False

        if User.get_email(data):
            flash('Email already taken', 'register')
            is_valid = False

        print('Validation: User is valid: ', is_valid)

        return is_valid

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM sasquatch.users;'
        results = connectToMySQL('sasquatch').query_db(query)

        users=[]

        for user in results:
            users.append(cls(user))

        return users
    
# ------------------------------

    @classmethod # this saves the data and updates the database with new information
    def save(cls, data):
        query = 'INSERT INTO sasquatch.users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        return connectToMySQL("sasquatch").query_db(query, data)

# ------------------------------