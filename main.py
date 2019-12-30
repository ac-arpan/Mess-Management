# This should be the main backend file.
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import os
from werkzeug import secure_filename
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mail import Mail,Message
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config.update(
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = '465',
        MAIL_USE_SSL = True,
        MAIL_USERNAME ="your@gmail.com",
        MAIL_PASSWORD = "type-your-password",
        )
mail = Mail(app)


# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mess'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialize MySQL
mysql = MySQL(app)

# check if user is logged-in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

# registration form made with flask-wtf


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    username = StringField('Username',[validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/register', methods=["GET", "POST"])
def register():
    # instance of the registration form(used in register.html)
    form = RegisterForm(request.form)
    if 'logged_in' in session:
        flash("You Are Already Logged In Please Logout to Register Again","danger")
    elif request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor

        cur = mysql.connection.cursor()

        # execute query
        cur.execute("INSERT INTO users(name,username,password,email) VALUES(%s, %s, %s, %s)",
                    (name, username, password, email))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('You are now registered and can login', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_candidate = form.password.data
        # create a cursor
        cur = mysql.connection.cursor()
        # get user by username
        result = cur.execute(
            "SELECT * from users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            name = data['name']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in'+" " + str(name), 'success')
                return redirect(url_for('index'))

            else:
                error = "Invalid login credential"
                return render_template('login.html', error=error,form=form)

            cur.close()
        else:
            error = "Username not found"
            return render_template('login.html', error=error,form=form)

    return render_template('login.html',form=form)


@app.route('/logout')
@is_logged_in            # user should be logged in to go to this route
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



@app.route('/forgot_route/',methods = ["GET","POST"])
def forgot_route():

    if request.method == "POST":
        email = request.form['email']

        cur = mysql.connection.cursor()
            
        result = cur.execute("SELECT * FROM users WHERE email = %s",[email])

        if result > 0:

            res = cur.fetchone()
            username = res['username']
            password =  res['password']

            msg = Message("Forgot Password - LeArN",
                        sender = "your@gmail.com",
                        recipients = [email])

            link = "http://127.0.0.1:5000/reset_password/" + password
            msg.body = 'Hello ' + username + ',\nYou or someone else has requested to reset password for your account.If it was you click the link : ' + link
            mail.send(msg)

            flash("A password-reset mail has been sent! Please click on the link given in the mail!",'success')
        else:
            error = "Email-id is not registered"
            return render_template('forgot_route.html',error=error)

       

    return render_template('forgot_route.html')




class ResetPasswordForm(Form):
    password = PasswordField('New Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm',message='Password do not match')
            ])
    confirm = PasswordField('Re-enter new password')  

@app.route('/reset_password/<path:password>/',methods = ["GET","POST"])
def reset_password(password):
    
    form = ResetPasswordForm(request.form)

    cur = mysql.connection.cursor()
            
    result = cur.execute("SELECT * FROM users WHERE password = %s",[password])

    username = cur.fetchone()['username']

    cur.close()


    if request.method == "POST":
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password=%s WHERE username=%s",(password,username))
        mysql.connection.commit()
        cur.close()
        flash("Your password is changed and updated. Please login!",'success')
        return redirect(url_for('login'))


    return render_template("reset_password.html",username=username,form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
