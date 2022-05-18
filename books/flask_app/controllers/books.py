from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author

# this route displays books.html
@app.route('/books')
def books():
    # call get_all() classmethod to display existing books
    return render_template('books.html', all_books = Book.get_all())

# this a POST route that will store the new book info
@app.route('/create/book', methods=['POST'])
def create_book():
    data = {
        "title": request.form['title'],
        "num_of_pages": request.form['num_of_pages']
    }
    Book.save(data)
    #class #function #pass in data/input
    return redirect('/books')

# this route will display/call a specific book and the authors who favor it
@app.route('/book/<int:id>')
def show_book(id):
    # we will use data dictionary to store the id
    data = {
        "id": id
    }
    # call the respective classmethods and pass "data" as the argument, assign the results to a new variable
    return render_template('book_favorites.html', this_book = Book.authors_who_fav(data), authors_not_associated = Author.authors_not_favored(data))

# this a POST route that saves the dropdown option to associate an excluded author with the book
@app.route('/add/author', methods=['POST'])
def add_author():
    data = {
        "author_id": request.form['author_id'],
        "book_id": request.form['book_id']
    }
    # call the respective classmethod and pass "data" as the argument
    Author.add_to_favorite(data)
    # use an f string to convert the book_id so that it can be redirected
    return redirect(f"/book/{request.form['book_id']}")
