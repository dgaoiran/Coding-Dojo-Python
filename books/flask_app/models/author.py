from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

#the Author class is used to create instances of new authors added to the db.
class Author:
#define all of the necessary columns to create a new author. base this on the ERD.
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # to hold/create a list of books associated with a specific author
        self.fav_books = []

#this classmethod is a function that will run a SQL query to get all authors
    @classmethod
    # cls (class) variable itself is the argument we use to pass through the function when we call on it
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books').query_db(query)
        # this is an empty list to store all instances of an author
        authors = []
        #create a for loop to append each class into the empty list as the results query runs
        # one_author is arbitrary
        for one_author in results:
            authors.append( cls(one_author))
        return authors

#this classmethod is a function that will save new instances of authors that are input into the form
    @classmethod
    # again, we pass the class itself along with an arbitrary var that will hold the data pertinent to the new class. in this case it's "data", and it represents %(name)s
    def save( cls, data ):
        # pretty straightforward here. write the insert query and assign results; exclude columns that AI. VALUES must align with the html values
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        results = connectToMySQL('books').query_db( query, data )
        return results

# this classmethod is a function that will assign an author to a book. This is to create a table of books that each authors favors (MANY TO MANY, as each can have multiple of the other)
# we WON'T need to rewrite this again in models/book.py
    @classmethod
    def add_to_favorite( cls, data ):
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);"
        results = connectToMySQL('books').query_db( query, data )
        # or I could just return the query above
        return results

# this classmethod is a function that will power the author_favorites page to show all books that the author favors
    @classmethod
    # var data passes the author_id selected by the user
    def get_favorite_books( cls, data):
        # what's happening? [RUN IN SQL FOR VISUAL]. We are selecting all authors, then LJ the favorites table onto authors, then LJ the books table onto favorites
        # It's expected to get duplicate columns!
        # We then pass data as the id after WHERE to specify the author
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books').query_db( query, data )
        # now we are using the first row in the results to create another instance of the author. cls() calls the __init__ function (OOP BABY!)
        # assign the instance to an arbitrary variable. in this case it is "author"
        author = cls(results[0])
        # now we need to create a for loop to run through each column from the results and store the data we want to display
        for r in results:
            # if statement will stop the function if there are no books to display. this means the selected author has no favorites
            if r['books.id'] == None:
                break
            # create new var to store the data into a dictionary as r moves through
            # we have to list out each column name, then specify the relevant table on the duplicate columns
            data = {
                "id": r['books.id'],
                "title": r['title'],
                "num_of_pages": r['num_of_pages'],
                "created_at": r['books.created_at'],
                "updated_at": r['books.updated_at']
            }
            #call on the author var
            #call the empty fav_books list we created and append instances of the Book class by the passing through the data collected
            author.fav_books.append( (data) )
            print(results)
        return author

### NINJA BONUS ###
#this classmethod is function that will display all authors that have not favored the book being viewed.
#We can write this in the book.py model, but I left if here since we are starting with the authors table
    @classmethod
    def authors_not_favored( cls, data):
    # whats' happening? we have to write two queries combined into one
    # the first query is to select all authors
    # NOT IN is keyword to only return the authors/results excluded from the second query
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        # assign results to an arbitrary var
        results = connectToMySQL('books').query_db( query, data )
        # we need an empty list to hold the author instances
        authors_excluded = []
        #create a for loop to append each class into the empty list as the results query runs
        for a in results:
            authors_excluded.append( cls(a) )
        return authors_excluded
