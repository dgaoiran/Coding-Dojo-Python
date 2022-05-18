from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja

class Dojo:

    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # We create a list so that later we can add in all the ninjas that are associated with a dojo.
        self.ninjas = []

## NEED TO SWAP KEYWORDS
# assign the db info to var 'results', create class var list[] to store instances as dojo moves through the results query
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        dojos = []
        for one_dojo in results:
            dojos.append( cls(one_dojo))
        return dojos

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        result = connectToMySQL('dojos_and_ninjas').query_db( query, data)
        return result

    @classmethod
    def get_dojo_with_ninjas( cls , data ):
        # query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db( query , data )
        # results will be a list of dojo objects with the ninja attached to each row. 
        # print(results)
        dojo = cls( results[0] )
        for db_row in results:
            # Now we parse the ninja  data to make instances of ninjas and add them into our list.
            # We have to specify the additional db for each identical column. Default db is dojos!
            n = {
                "id" : db_row["ninjas.id"],
                "first_name" : db_row["first_name"],
                "last_name" : db_row["last_name"],
                "age" : db_row["age"],
                "created_at" : db_row["ninjas.created_at"],
                "updated_at" : db_row["ninjas.updated_at"]
            }
            dojo.ninjas.append( Ninja(n) )
            # var  #db           #Class # data dict holding parsed data per ninja
        return dojo