from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.dojo import Dojo

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    # call the get all classmethod to get all dojos
    dojos = Dojo.get_all()
    # print(dojos)'Dojo'
    return render_template("index.html", all_dojos = dojos)

## NEED POST ROUTE TO SAVE/CREATE DOJO

@app.route('/create/dojo',methods=['POST'])
def create_dojo():
    Dojo.save(request.form)
    #class #function #pass in data/input
    return redirect('/dojos')

# Below is a function that will go to the single dojo display 
# with all ninjas in that location
@app.route('/dojo/<int:id>')
def show_dojo(id):
    # create a dictionary to store the id that we pass from the route,
    # which is the id retrieved from index.html/database
    database = {
        "id": id
    }
    # dojo = Dojo.get_dojo_with_ninjas(data)
    return render_template('dojo.html', dojo = Dojo.get_dojo_with_ninjas(database))