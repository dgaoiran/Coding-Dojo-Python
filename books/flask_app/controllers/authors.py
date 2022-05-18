from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

# this route redirects to /authors
@app.route('/')
def index():
    return redirect('/authors')

# this route displays the index page
@app.route('/authors')
def authors():
    #upon calling this function, we're also calling get_all() classmethod from Author class
    #we can assign the query results to a variable that will be referenced in html
    return render_template ('index.html', all_authors = Author.get_all())

# this a POST route that will store the new author's name
@app.route('/create/author', methods=['POST'])
def create_author():
    data = {
        "name": request.form['name']
    }
    Author.save(data)
    #class #function #pass in data/input
    return redirect('/authors')

# this route  will display/call a specific author and the books they favored
@app.route('/author/<int:id>')
def show_author(id):
    # we will use data dictionary to store the id
    data = {
        "id": id
    }
    # call the respective classmethods and pass "data" as the argument, assign the results to a new variable
    return render_template('author_favorites.html', this_author = Author.get_favorite_books(data), unfavored_books = Book.books_not_favored(data))

# this a POST route that saves the dropdown option to add an excluded book to the author's fav
@app.route('/add/book', methods=['POST'])
def add_book():
    data = {
        "author_id": request.form['author_id'],
        "book_id": request.form['book_id']
    }
    # call the respective classmethod and pass "data" as the argument
    Author.add_to_favorite(data)
    # use an f string to convert the author_id so that it can be redirected
    return redirect(f"/author/{request.form['author_id']}")
