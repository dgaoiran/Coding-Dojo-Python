from flask import render_template, redirect, request
from flask_app import app
from flask_app.models import dojo, ninja


@app.route("/ninjas")
def new_ninja():
    return render_template("ninja.html", dojos = dojo.Dojo.get_all())
                                        #var #dojo.py #Class #function to get all dojos

@app.route("/create/ninja", methods=['POST'])
def create():
    ninja.Ninja.save(request.form)
    return redirect('/')