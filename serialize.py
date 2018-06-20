'''
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

    def __init__(self, goalscorer, minute, round):
        self.goalscorer = goalscorer
        self.minute = minute
        self.round = round
'''
