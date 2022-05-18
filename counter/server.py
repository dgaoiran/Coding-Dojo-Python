from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'goWarriors'

@app.route('/')
def index():
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1
    return render_template("index.html")

@app.route('/destroy_session', methods=['POST'])
def destroy():
    session.pop('count')
    return redirect('/')

@app.route('/add_2', methods=['POST'])
def add_2():
    session['count'] += 1
    return redirect('/')

@app.route('/increment', methods=['POST'])
def increment():
    session['numbers'] = int(request.form['number'])
    num = session['numbers']
    session['count'] += num -1
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
