from json import dumps
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/wcdatadash'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Goal(db.Model):
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
        self.goalscorer = goalscorer
        self.minute = minute
        self.method = method
        self.round = round
        self.country = country
        self.continent = continent
        self.phase = phase

def goals_to_json(goal):
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
    return render_template('goals.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/goalsdata')
def get_goals_json():
    return goals_to_json(Goal)

if __name__ == '__main__':
    app.debug = True
    app.run()
