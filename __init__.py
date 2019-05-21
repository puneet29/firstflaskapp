from flask import Flask, render_template, request, url_for, redirect
from content_management import Content

app = Flask(__name__)
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

        if request.method == "POST":

            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))

            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)
