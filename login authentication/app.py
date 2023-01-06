from flask import Flask, redirect, render_template, request, flash, url_for
from flask_login import login_manager, login_required, UserMixin, LoginManager
import sqlite3
import datetime
app = Flask(__name__)
app.secret_key="secrete-key"

login = LoginManager(app)

class User(UserMixin):
    def __init__(self,fname,lname,email,password,isactive) -> None:
        super().__init__()
        self.name = fname+lname
        self.email = email
        self.password = password
        self.active = isactive

    def is_authenticated(self):
        return True

@login.user_loader
def load_user(user):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user,))
    user = c.fetchone()
    if user:
        return User(user[1], user[2], user[5], user[6], user[4])
    return None


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method =='POST':
        email =request.form['email']
        password = request.form['password']
        lname= request.form['lname']
        fname =request.form['fname']
        date = datetime.datetime.now()
        conn = sqlite3.connect('mydatabase.db')
        c =conn.cursor()
        c.execute('SELECT * from users where email=?',(email,))
        user = c.fetchone()
        if user :
            flash('Already Registred','login')
        else:
            c.execute('INSERT INTO users (fname, lname, email, password, date) VALUES(?,?,?,?,?);',(fname, lname, email, password, date))
            conn.commit()
            conn.close()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email =request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('mydatabase.db')
        c =conn.cursor()
        c.execute('SELECT email, password, is_active from users where email=?',(email,))
        user = c.fetchone()
        if email == user[0] and password== user[1]:
            if user[2] == 0:
                flash('Active account first','active')
            return redirect(url_for('index'))
        else:
            flash("wrong credentials", 'error')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
    