from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from flask_app.models import recipe

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.cook_time = data['cook_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # placeholder representing a User
        self.user = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, cook_time, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(cook_time)s, %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)

# # this method will get all recipes
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM recipes WHERE user_id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        all_recipes = []
        for one_recipe in results:
            all_recipes.append( cls(one_recipe))
        return all_recipes

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, cook_time = %(cook_time)s WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

# this method will retrieve a single recipe by its id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return results

### STATICMETHODS ###

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if recipe['name'] == "":
            flash("Name must be at least 3 charaters.", "recipe")
            is_valid = False
        if recipe['description'] == "":
            flash("Description must be at least 3 charaters", "recipe")
            is_valid = False
        if recipe['instructions'] == "":
            is_valid = False
            flash("Instrcutions must be at least 3 charaters", "recipe")
        if recipe['date_made'] == "":
            flash("Please enter date", "recipe")
            # flash("Please select one", "recipe")
            # is_valid = False
        return is_valid