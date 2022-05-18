from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/play')
# Level 1
@app.route('/play')
def play():
    return render_template("index.html", num=3, color="aqua")

# Level 2
@app.route('/play/<int:banana>')
def play_2(banana):
    return render_template("index.html", num=banana, color="aqua")

# Level 3
@app.route('/play/<int:num>/<string:fill>')
def play_3(num, fill):
    return render_template("index.html", num=num, color=fill)

if __name__=="__main__":
    app.run(debug=True)
