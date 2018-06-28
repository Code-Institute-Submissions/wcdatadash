"""
A simple script to help fill the database with data
"""

from app import db, Goal, Team

class Admin(object):
    """
    This class allows for a continuous entry of goals to the database. It basically switches between the home and add_goal
    methods based on the users command. One data is entered correctly, a success message will display. 
    """
    def home(self):
        """
        The main menu
        """
        print("""
DATA ENTRY ADMIN
----------------
Choose an option:
    Add (g)oal
    or (q)uit
""")
        choice = raw_input('Choice: ')

        if choice.lower() == 'g':
            self.add_goal()
                
        elif choice.lower() == 'q':
            print('Goodbye')
        
        else:
            print("{} is not an option!".format(choice.lower))
            self.home()

    def add_goal(self):
        """
        The user fills in the fields using the raw_input function and the transaction with the database is performed automatically 
        """
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

        try:
            db.session.commit()
            raw_input('Goal by {} added successfully!'.format(goalscorer))
        except Exception as e:
            print(e)
            raw_input('There appears to have been an error..')

        self.home()
    
    

if __name__ == '__main__':
    Admin().home()