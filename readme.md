# WCGoals DataDash

## Intro

Using goals scored data from the Fifa World Cup 2018 in Russia. I have created a data dash-board using D3.js, DC.js and Crossfilter. The site has been created with Python using the Flask web framework, and has been deployed using Heroku.

As the charts update upon filtering, you can explore patterns in how the goals were scored based on a variety of factors. Such as the minute scored, the current round, the country or continent etc

[Visit site..](https://wcgoals-datadash.herokuapp.com/)

## To use

The page boots with a tutorial upon visiting. Follow the simple instructions to use. 

## Creation

My initial setup and help with deployement owes to [sahildiwan's blog](http://blog.sahildiwan.com/posts/flask-and-postgresql-app-deployed-on-heroku/). I gained inspiration from his app file setup and changed the routes to fit my need.

## Installing on your machine

First you will need to 
[get pip](https://pip.pypa.io/en/stable/installing/)
and
[Postgresql](https://www.postgresql.org/download/)

CD to your desired folder and run the following from the terminal:

`git clone https://github.com/danieldeiana/wcdatadash.git`

Activate the virtual environment:

`. myenv/bin/activate`

To run the app locally go to the app.py file in the root folder and change the LOCAL variable to True. Then run the app from the terminal:

`python app.py`

and visit [local host](http://127.0.0.1:5000/) in your favourite browser.

To run the tests go to the root folder in the terminal and run:

`python tests.py`

### Use data locally

If you would like to use the goals data locally you can link to it as so..

At the top of the app.py file, `import urllib`

Change the get_goals_json() function from this:

```
@app.route('/goalsdata')
def get_goals_json():
    """
    When accessing this route, the serialized Goal object is provided
    """
    return goals_to_json(Goal)
```

to this:

```
@app.route('/goalsdata')
def get_goals_json():
    """
    When accessing this route, the serialized Goal object is provided
    """
    link = 'https://wcgoals-datadash.herokuapp.com/goalsdata'
    open_link = urllib.urlopen(link)
    goals_data = open_link.read()
    return goals_data
```
