import unittest
from json import dumps
from app import app, db, Goal, goals_to_json

class appTests(unittest.TestCase):
    def test_views_response_status(self):
        client = app.test_client(self)

        resp = client.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)

        resp = client.get('/about', content_type='html/text')
        self.assertEqual(resp.status_code, 200)

        resp = client.get('/goalsdata', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
    
    def test_goals_to_json_function(self):
        a_goal = Goal.query.all()[0]
        try:
            a_goal_parsed_to_json = goals_to_json(a_goal)
        except Exception as e:
            print('Failed to parse to json with error: {}'.format(e.message))
        
    def test_view_goalsdata_returns_valid_json(self):
        client = app.test_client(self)

        resp = client.get('/', content_type='json')
        try:        
            json_data = dumps(resp.data)
        except Exception as e:
            print('Failed to parse to json with error: {}'.format(e.message))

if __name__ == '__main__':
    unittest.main()