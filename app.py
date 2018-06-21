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

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    total_shots = db.Column(db.Integer)
    shots_on_target = db.Column(db.Integer)
    possesion = db.Column(db.Integer)
    total_passes = db.Column(db.Integer)
    yellows = db.Column(db.Integer)
    reds = db.Column(db.Integer)

    def __init__(self, name, wins, draws, losses, total_shots, shots_on_target, possesion, total_passes, yellows, reds):
        self.name = name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.total_shots = total_shots
        self.shots_on_target = shots_on_target
        self.possesion = possesion
        self.total_passes = total_passes
        self.yellows = yellows
        self.reds = reds

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

def teams_to_json(team):
    teams = team.query.all()
    team_list = []

    for team in teams:
        team_dict = {}
        team_dict['id'] = team.id
        team_dict['name'] = team.name
        team_dict['wins'] = team.wins
        team_dict['draws'] = team.draws
        team_dict['losses'] = team.losses
        team_dict['total_shots'] = team. total_shots
        team_dict['possesion'] = team.possesion
        team_dict['total_passes'] = team.total_passes
        team_dict['yellows'] = team.yellows
        team_dict['reds'] = team.reds
        
    return dumps(team_list)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/goals')
def get_goals_json():
    return goals_to_json(Goal)


if __name__ == '__main__':
    app.debug = True
    app.run()
