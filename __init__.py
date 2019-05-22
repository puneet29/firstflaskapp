from flask import Flask, render_template, request, url_for, redirect, flash, session
from content_management import Content
from dbconnect import connection
from wtforms import Form, TextField, PasswordField, validators, BooleanField
from passlib.hash import sha256_crypt
import gc


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(
        min=6, max=50), validators.Email(), validators.Required()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField(
        'I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

TOP_DICT = Content()


@app.route('/')
def homepage():
    return render_template('main.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html', TOP_DICT=TOP_DICT)


@app.route('/login/', methods=["GET", "POST"])
def login_page():

    error = ''
    try:
        c, conn = connection()
        if(request.method == "POST"):
            c.execute('SELECT * FROM users WHERE username=(%s)', (request.form['username'], ))
            data = c.fetchone()

            if(data != None):
                if(sha256_crypt.verify(request.form['password'], data[2])):
                    session['logged_in'] = True
                    session['username'] = request.form['username']

                    flash("You are now logged in!")
                    return(redirect(url_for("dashboard")))

                else:
                    error = "Invalid Credentials. Please try again!"
            else:
                error = "User doesn't exist."

        gc.collect()

        return(render_template("login.html", error=error))
    except Exception as e:
        # flash(e)
        error = "Some error occurred. Please try again! Raise a descriptive issue at https://www.github.com/puneetsaini/firstflaskapp"
        return render_template("login.html", error=error)


@app.route('/signup/', methods=["GET", "POST"])
def signup_page():
    try:
        form = RegistrationForm(request.form)
        if (request.method == "POST" and form.validate()):
            username = form.username.data.lower()
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            c.execute('SELECT * FROM users WHERE username=(%s)', (username, ))
            rows = c.fetchall()

            if (len(rows) > 0):
                flash("Username already taken. Please choose another.")
                return(render_template('signup.html', form=form))
            else:
                c.execute('INSERT INTO users(username, password, email, tracking) VALUES(%s, %s, %s, %s)',
                          (username, password, email, "/dashboard/"))
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username
                return(redirect(url_for('dashboard')))

        return(render_template('signup.html', form=form))

    except Exception as e:
        # return(str(e))
        return(render_template("500.html"))


if __name__ == "__main__":
    app.run(debug=True)
