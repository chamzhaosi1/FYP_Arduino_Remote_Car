## Refer: https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<User {self.password}>'

@app.route('/')
def home():
    # if 'username' in session:
    #     user_detail = session['username'] 
    #     romo_detail = {
    #         "mac_add" : "00:B0:D0:63:C2:26".upper(),
    #         "status" : "Idle".upper(),
    #         "dev_name" : "Room".upper()
    #     }
    
    #     return render_template('dashboard.html', 
    #                            username=session['username'], 
    #                            title="Dashboard", 
    #                            type="Dashboard",
    #                            user_detail=user_detail.upper(),
    #                            romo_detail=romo_detail)
    # else:
    #     return redirect('/login')
     return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html', title="Login", type="Login")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')
    else:    
        return render_template('register.html', title="Register", type="Register")
    
@app.route('/live_streaming', methods=['GET','POST'])
def live_streming():
    if 'username' in session:
        user_detail = session['username'] 
        return render_template('live_streaming.html', 
                               title="Live Streaming",
                               user_detail=user_detail.upper(), 
                               type="Live Streaming",)
    else:
        return redirect('/login')

@app.route('/event', methods=['GET','POST'])
def event():
    if 'username' in session:
        user_detail = session['username'] 
        return render_template('event.html', 
                               title="Event",
                               user_detail=user_detail.upper(), 
                               type="Event",)
    else:
        return redirect('/login')