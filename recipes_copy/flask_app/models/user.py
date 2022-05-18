from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
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

        self.saved_recipes = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes').query_db(query, data)
        return results

# this method will retrieve a single user by their email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        # if stataement to validdate if email is already in the db
        if len(results) < 1:
            return False
        return cls(results[0])

# this method will retrieve a single user by their id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_saved_recipes(cls):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query)

        user = cls(results[0])

        for r in results:
            if r['recipes.id'] == None:
                break

            data = {
                "name": r['name'],
                "cook_time": r['cook_time'],
            }
            user.saved_recipes.append( (data) )
            print(data)
        return user

### STATICMETHODS BELOW ###
    @staticmethod
    def validate_user(user):
        # we assume this is true
        is_valid = True
        # run a query to check if the email already exists in the db
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, user)
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
            flash("Password do not match", "register")
        return is_valid