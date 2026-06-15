from flask import render_template   
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'Cupcake'},
            'body': 'Mreow'
        },
        {
            'author': {'username': 'Tammy'},
            'body': 'Purrrr'
        },
        {
            'author': {'username': 'Coco'},
            'body': 'You know we are fake posts in a flask application, right?'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)