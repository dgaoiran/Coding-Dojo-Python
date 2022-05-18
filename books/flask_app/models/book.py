from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

#Book class is used to create instances of new books added to the db.
class Book:
#define all of the necessary columns to create a book. base this on the ERD.
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # to hold/create a list of authors associated with a specific book
        self.authors_who_fav = []

#this classmethod is a function that will run a SQL query to get all books; this will be used on books.html
    @classmethod
    # cls (class) variable itself is the argument we use to pass through the function when we call on it. we don't have to include data because we're only retrieving from db
    def get_all(cls):
        query = "SELECT * FROM books;"
        # we are assinging the query results to a variable
        results = connectToMySQL('books').query_db(query)
        # this is an empty list to store all instances of a book
        books = []
        #create a for loop to append each class into the empty list as the results query runs
        # one_author is arbitrary
        for one_book in results:
            books.append( cls(one_book))
        return books
    
#this classmethod is a function that will save new instances of books that are input into the form
    @classmethod
    # again, we pass the class itself along with an arbitrary var that will hold the data pertinent to the new class. 
    # in this case it's "data", and it represents %(title)s, %(num_of_pages)s
    def save( cls, data ):
        # pretty straightforward here. write the insert query and assign results; exclude columns that AI. VALUES must align with the html values
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        results = connectToMySQL('books').query_db( query, data )
        # can also immediately return query
        return results

# this classmethod is a function that will power the book_favorites page to show all the authors who favor that book
    @classmethod
    # var data passes the book_id selected by the user
    def authors_who_fav( cls, data):
        # what's happening? [RUN IN SQL FOR VISUAL]. We are selecting all books, then LJ the favorites table onto books, then LJ the authors table onto favorites
        # It's expected to get duplicate columns!
        # We then pass data as the id after WHERE to specify the relevant book
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL('books').query_db( query, data )
        # now we are using the first row in the results to create another instance of *that* book. cls() calls the __init__ function (OOP BABY!)
        # assign the instance to an arbitrary variable. in this case it is "book"
        book = cls(results[0])
        # now we need to create a for loop to run through each column from the results and store the data we want to display. 
        for r in results:
            #  if statement will stop the function if there are no authors to display. this means the selected book has no authors who fav
            # format is tablenameplural.id
            if r['authors.id'] == None:
                break
            # create new var to store the data into a dictionary as r loops through
            # we have to list out each column name, then specify the relevant table on the duplicate columns
            data = {
                "id": r['authors.id'],
                "name": r['name'],
                "created_at": r['authors.created_at'],
                "updated_at": r['authors.updated_at']
            }
            #call on the book var
            #call the empty list "authors_who_fav" we created and append instances of the Author class by the passing through the data collected
            book.authors_who_fav.append( (data) )
            print(data)
        return book
### NINJA BONUS ###

#this classmethod is function that will display all the books that the author hasn't favored. this will be used in the dropdown of author_favorites
#summary: pull all authors then omit the ones that the author already favored
    @classmethod
    def books_not_favored( cls, data):
    # whats' happening? we have to write two queries combined into one
    # the first query is to select all books
    # NOT IN is keyword to only return the books/results excluded from the second query
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"
        # assign results to an arbitrary var
        results = connectToMySQL('books').query_db( query, data )
        # we need an empty list to hold the book instances
        books_excluded = []
        #create a for loop to append each class into the empty book list as the results query runs
        for b in results:
            books_excluded.append( cls(b) )
        print(results)
        return books_excluded