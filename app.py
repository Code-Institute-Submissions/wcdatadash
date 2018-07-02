from json import dumps
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

LOCAL = False

if LOCAL:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/wcdatadash'

else:
    heroku = Heroku(app)

db = SQLAlchemy(app)

class Goal(db.Model):
    """
    The Goal model inheriting SQLAlchemy instantiated with the  created Flask app
    """
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    goalscorer = db.Column(db.String(60))
    minute = db.Column(db.Integer)
    method = db.Column(db.String(60))
    round = db.Column(db.String(60))
    country = db.Column(db.String(60))
    continent = db.Column(db.String(60))
    phase = db.Column(db.String(60))

    def __init__(self, goalscorer, minute, method, round, country, continent, phase):
        """
        When initializing a Goal model object, fill all the fields in the first instance. 
        """
        self.goalscorer = goalscorer
        self.minute = minute
        self.method = method
        self.round = round
        self.country = country
        self.continent = continent
        self.phase = phase

def goals_to_json(goal):
    """
    Serialize a Goal object to JSON
    """
    goals = goal.query.all()
    goals_list = []

    for goal in goals:
        goal_dict = {}
        goal_dict['id'] = goal.id
        goal_dict['goalscorer'] = goal.goalscorer
        goal_dict['minute'] = goal.minute
        goal_dict['method'] = goal.method
        goal_dict['round'] = goal.round
        goal_dict['country'] = goal.country
        goal_dict['continent'] = goal.continent
        goal_dict['phase'] = goal.phase
        goals_list.append(goal_dict)
    
    return dumps(goals_list)

@app.route('/')
def goals():
    """
    The index route which displays the dash-board
    """
    return render_template('goals.html')

@app.route('/about')
def about():
    """
    An about page which provides additional information about the website
    """
    return render_template('about.html')

@app.route('/goalsdata')
def get_goals_json():
    """
    When accessing this route, the serialized Goal object is provided
    """
    return goals_to_json(Goal)

if __name__ == '__main__':
    app.debug = True
    app.run()
