from app import db, Goal, Team

class Admin(object):
    def home(self):
        print("""
DATA ENTRY ADMIN
----------------
Choose an option:
    Add (g)oal
    Add (t)eam Stats for a match
    or (q)uit
""")
        choice = raw_input('Choice: ')

        if choice.lower() == 'g':
            self.add_goal()
        
        elif choice.lower() == 't':
            self.increment_team_stats()
        
        elif choice.lower() == 'q':
            print('Goodbye')
        
        else:
            print("{} is not an option!".format(choice.lower))
            self.home()

    def add_goal(self):
        goalscorer = raw_input('Who scored? ')
        minute = raw_input('Minute: ')
        method = raw_input('Method ie. header, outside box, inside box, freekick: ')
        round = raw_input('round from 1-4, and quarter, semi and final: ')
        country = raw_input('country that scored: ')
        continent = raw_input('continent the country are from: ')
        phase = raw_input('phase ie counter, set-piece, open-play: ')

        goal = Goal(
            goalscorer,
            minute,
            method,
            round,
            country,
            continent,
            phase
        )

        db.session.add(goal)
        db.session.commit()

        raw_input('Goal by {} added successfully!'.format(goalscorer))

        self.home()
    
    def increment_team_stats(self):
        '''
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
        '''
        seperation = 90
        print('-' * seperation)
        print('Enter stats on a game by game basis. Entered stats will increment to the original values.')
        print('-' * seperation)

        teams = Team.query.all()
        print('\n')
        for team in teams:
            print(team.name)
        team = raw_input('\nWhich teams stats to increment? ')
        chosen_team = Team.query.filter_by(name=team).first()

        if not chosen_team:
            print('{} is not in the World Cup! Have you spelled it correctly?')
            raw_input('   - press enter -')
            self.increment_team_stats()
        
        wins, draws, losses = (0, 0, 0)
        
        win_lose_or_draw = raw_input('(w)in (l)ose or (d)raw? ')
        if win_lose_or_draw.lower() == 'w':
            wins = 1
        elif win_lose_or_draw.lower() == 'l':
            losses = 1
        elif win_lose_or_draw.lower() == 'd':
            draws = 1
        else:
            raw_input('Please enter w, l or d. Not {}'.format(win_lose_or_draw))
            self.increment_team_stats()

        total_shots = int(raw_input('Total shots: '))
        shots_on_target = int(raw_input('Shots on target: '))
        possesion = int(raw_input('Possesion: '))
        total_passes = int(raw_input('Total passes: '))
        yellows = int(raw_input('Yellows: '))
        reds = int(raw_input('Reds: '))
        
        chosen_team.wins += wins
        chosen_team.draws += draws
        chosen_team.losses += losses
        chosen_team.total_shots += total_shots
        chosen_team.shots_on_target += shots_on_target
        chosen_team.possesion += possesion
        chosen_team.total_passes += total_passes
        chosen_team.yellows += yellows
        chosen_team.reds += reds

        db.session.add(chosen_team)
        db.session.commit()

        print('{} stats updated sucsessfully!'.format(chosen_team.name))
        raw_input('   - press enter -')
        self.home()

if __name__ == '__main__':
    Admin().home()