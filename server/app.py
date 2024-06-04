# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False   #! a configuration that has JSON responses print on separate lines with indentation. This adds some overhead, but if human eyes will be looking at your API, it's always good to have this set to False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

#?----------------------------------------------------------------------
@app.route('/games')
def games():

    #? Our query results have to be reformatted as dictionaries for jsonify to work its magic. 
    #!The __dict__ attribute cannot be used here because SQLAlchemy records have attributes that are nonstandard Python objects.
    #? We're leaving game.id out here because game.title is already set to unique.


    games = [game.to_dict() for game in Game.query.all()]

    response = make_response(
        games,
        200,
        {"Content-Type": "application/json"}  # Uneeded but is just to show what is happening behind the scenes
    )

    #!!!!!!! jsonify() is now run automatically on all dictionaries returned by Flask views. We'll just pass in those dictionaries from now on, but remember what jsonify()'s doing for you behind the scenes!

    #? Example returns I can do
    games_by_title = Game.query.order_by(Game.title).all() #* sort the games by title
    first_2_games = Game.query.limit(2).all() #* return the first 2 games

    return response

#?-------------------------------------------------------------------------
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first() #! Always query for a unique attribute in a filter statement

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

