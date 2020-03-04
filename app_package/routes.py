from flask import render_template, flash, redirect, url_for
from app_package import app
from app_package.forms import LoginForm
from app_package.TWEEZER import get_profile, get_profileTwython
import tweepy

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
def error():
    return render_template('error.html')


@app.route('/', methods= ['GET', 'POST']) # !
@app.route('/login', methods= ['GET', 'POST'])
def login():

    form= LoginForm()


    if form.validate_on_submit():
                
        try:
            try: 
                print('Consultando el perfil usando Tweepy.')
                user_1 = get_profile(form.username.data)
                print('Perfil consultado usando Tweepy.\n')
            except:
                print('No se encontró el perfil x Tweepy.\n')
                return redirect(url_for('error'))

        except tweepy.TweepError:
            print('TweepError')
            return redirect(url_for('error'))
  

        try:
            print('Consultando el perfil usando Twython')
            user_2= get_profileTwython(form.username.data)
            print('Perfil consultado usando Twython\n')
        except:
            print('No se encontró el perfil x por Twython\n')    

    

        return render_template('principal.html', title= 'MIMTA R', user_1= user_1, user_profileTw= user_2 )
    return render_template('login.html', title= 'Sign in', form= form)