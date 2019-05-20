from flask import Flask, render_template

app = Flask(__name__)


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
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
