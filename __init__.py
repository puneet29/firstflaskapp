from flask import Flask, render_template
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
    return render_template('dashboard.html', TOP_DICT= TOP_DICT)


if __name__ == "__main__":
    app.run(debug=True)
