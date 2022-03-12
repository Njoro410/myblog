from flask import Blueprint, render_template

from app.request import get_quotes



views = Blueprint('views', __name__)

@views.route('/')
def index():
    quote = get_quotes()
    
    
    
    return render_template('index.html',quote=quote)

