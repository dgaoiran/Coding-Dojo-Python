from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app.models.user import User


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

# this is a POST route will use session to measure T/F
@app.route('/submit',  methods=['POST'])
def submit():
    # check to see if the login email input is in the db and assign to a var 
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    session['user_id'] = user.id
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/welcome')

# this route will passes the user_id so that can call it in html
@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('welcome.html', user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

@app.route('/register', methods=['POST'])
def register_user():
    # call the staticmethod to validate
    # this is taking the input and passing it through
    if not User.validate_user(request.form):
        return redirect('/')
        # redirect to the route where the burger form is rendered #
    # else if valid:
    # create a new instance of the user by passing data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    # call the save function and assign the returned id into a var
    id = User.save(data)
    # save the var into session
    session['user_id'] = id
    return redirect('/welcome')

