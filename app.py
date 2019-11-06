from flask import Flask, render_template
from src import database as dp
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/check_user', methods=['POST'])
def print_user_details():
    if request.method == 'POST':
        if request.form['username'] != "":
            username = request.form['username']
            password = request.form['password']
        return render_template('user_home.html', username=username, password=password)
if __name__ == '__main__':
    app.run()