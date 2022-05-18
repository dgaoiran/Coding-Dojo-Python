from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# regex module
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('login_and_registration').query_db(query, data)
    
# this method will retrieve a single user by their email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

# this method will retrieve a single user by their id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('login_and_registration').query_db(query, data)
        return cls(results[0])

### Static methods don't have self or class passed into the parameters so we pass any var
    @staticmethod
    def validate_user(user):
        # we assume this is true
        is_valid = True
        # run a query to check if the email already exists in the db
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('login_and_registration').query_db(query, user)
        # if statement; 1 is occupied
        if len(results) >= 1:
            flash("Email is already taken.", "register")
            # if this if statement is false, then it's open
            is_valid = False
        # if statement to check email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        # if statement to compare password inputs
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match","register")
        return is_valid
