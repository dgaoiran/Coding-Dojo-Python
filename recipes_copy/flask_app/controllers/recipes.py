from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "id": session['user_id']
    }
    data = {
        "id": id
    }
    return render_template('view_recipe.html', this_recipe=Recipe.get_by_id(data), this_user=User.get_by_id(user_id))

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    return render_template('edit_recipe.html', this_recipe=Recipe.get_by_id(data))

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
        # now we are calling the validate_recipe function
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        "id": id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "cook_time": request.form['cook_time'],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    # now we are calling the validate_recipe function
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "cook_time": request.form['cook_time'],
        "user_id": session['user_id']
    }
    recipe = Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes/destroy/<int:id>')
def destroy(id):
    data = {
        "id": id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')