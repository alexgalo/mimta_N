from flask import render_template
from app_package import app


@app.route('/index')
def index():
    user = {'username': 'Félix'}
    # lista
    posts = [
        {
            'author': {'username': 'Caro'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('principal.html', title='Home', user=user, posts=posts)

@app.route('/aboutme')    
def aboutme():
    return render_template('aboutme.html')

@app.route('/error')
def error_0():
    return render_template('error.html')

@app.route('/error_')
def error_1():
    return render_template('error.html')

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')