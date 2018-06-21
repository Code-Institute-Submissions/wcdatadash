from app import *

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
            self.add_team_stats()
        
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
    
    def add_team_stats(self):
        print 'Add team stats'

        self.home()

if __name__ == '__main__':
    Admin().home()