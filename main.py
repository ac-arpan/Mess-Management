from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
import os
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from passlib.hash import sha256_crypt
from datetime import datetime

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


@app.route('/',methods = ["GET","POST"])
def index():
    
    l = []
    for i in range(1,32):
        l.append(i)

    # user registration starts here
    if  request.method == 'POST':
        if request.form['btn'] == 'Register':
            name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            password = sha256_crypt.encrypt(str(request.form['password']))

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

    #user registration ends here

    #user login starts here

        elif  request.form['btn'] == 'Login':
            username = request.form['lUsername']
            password_candidate = request.form['lPassword']
            # create a cursor
            cur = mysql.connection.cursor()
            # get user by username
            result = cur.execute("SELECT * from users WHERE username = %s", [username])
            
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
                    return render_template('index.html', error=error,dates=l)

                cur.close()
            else:
                error = "Username not found"
                return render_template('index.html', error=error,dates=l)

        elif  request.form['btn'] == 'Reset Password':
            email = request.form['forgotEmail']
            print(email)
            flash("A mail has been sent!",'success')
            return redirect(url_for('index'))

    # user login ends here

    return render_template('index.html',dates=l)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    
    # create a cursor
    cur = mysql.connection.cursor()
    # get user by username
    cur.execute("SELECT * from users WHERE username = %s", [session['username']])
    data = cur.fetchone()
    return render_template('profile.html',data=data)

app.run(debug=True)