from flask import Flask, render_template,request
from src import database as dp
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("login-page.html")
@app.route('/registration')
def reg():
    return render_template("registration-page.html")
@app.route('/hello', methods=['POST'])
def welcome():
    user = request.form['username']
    return render_template('welcome-page.html', username=user)


@app.route('/check_user', methods=['POST'])
def print_user_details():
    if request.method == 'POST':
        if request.form['username'] != "":
            username = request.form['username']
            password = request.form['password']
        return render_template('user_home.html', username=username, password=password)
if __name__ == '__main__':
    app.run()