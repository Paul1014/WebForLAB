# save this as app.py
from flask import Flask
from flask import render_template,redirect,url_for,request
from flask_login import  UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import json
import time
from flask_socketio import SocketIO, emit


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'Skills39'
socketio = SocketIO(app)

### Example User ###
users = {'admin': {'password': 'admin'}} 

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(login_user):
    if login_user not in users:
        return
    user = User()
    user.id = login_user
    return user

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if current_user.is_active:
        return redirect(url_for('protected'))
    else:
        if request.method == 'GET':
            return render_template('login.html',failinfo=" ")
        else:
            username = request.form['username']
            password = request.form['password']
        try:
            if password == users[username]['password']:
                user = User()
                user.id = username
                login_user(user)
                return redirect(url_for('protected'))  
            else:
                return render_template('login.html', failinfo="Password is not correct! Try again.")
        except:
                return render_template('login.html', failinfo="Cannot found this Username, plz check.")

@app.route('/protected')  
@login_required  
def protected():  
    #  current_user確實的取得了登錄狀態
    if current_user.is_active:  
        return 'Logged in as: ' + current_user.id + 'Login is_active:True <br> <a href=logout>Logout</a> <br> <a href=ws>websocket</a>'


@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('login'))


@app.route("/timeout")
def timeout():
    time.sleep(300)
    return "timeout"

@app.route("/ws", methods=['GET'])
def ws():
    if current_user.is_active:
        return render_template('websocket.html')
    else:
        return "please fking login"


@socketio.on('send')
def chat(data):
    socketio.emit('get', data)


@socketio.on('test')
def test():
    socketio.send("test")


if __name__ == '__main__':
    socketio.run(app)