from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    #example challenge below:
    challenges = [
    {
        "title": "My Test Challenge",
        "startArticle": "University",
        "endArticle": "Bottled Water",
        "guesses": 6,
        "creator": "Joseph",
        "timeLeft": "2 hours 13 minutes"
    },{
        "title": "My Test Challenge Again!",
        "startArticle": "Library",
        "endArticle": "Wisdom Teeth",
        "guesses": 1,
        "creator": "Not Joseph",
        "timeLeft": "13 minutes"
    }]
    return render_template("index.html", challenges=challenges)