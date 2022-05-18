from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app = Flask(__name__)
app.secret_key = 'goWarriors' # set a secret key for security purposes

# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    print(request.form)
    session['username'] = request.form['name']
    session['useremail'] = request.form['email']
# Never render a template on a POST request.
# Instead we will redirect to our index route.
    return redirect("/show")

@app.route("/show")
def show_user():
    return render_template("show.html")

if __name__ == "__main__":
    app.run(debug=True)
