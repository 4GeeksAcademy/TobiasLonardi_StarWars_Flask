"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/health-check", methods=["GET"])
def health_check():
    return jsonify("ok"), 200

@app.route("/people", methods=["GET"])
def getCharacter():
    characters=Character.query.all()
    return jsonify([item.serialize() for item in characters]), 200

@app.route("/people/<int:id>", methods=["GET"])
def get_one_character(id=None):
    character=Character.query.get(id)
    if(character is None):
        return jsonify("character not found"), 404
    
    return jsonify(character.serialize()), 200

@app.route("/planet", methods=["GET"])
def getPlanet():
    planets=Planet.query.all()
    return jsonify([item.serialize() for item in planets]), 200


@app.route("/planet/<int:id>", methods=["GET"])
def get_one_planet(id=None):
    planet=Planet.query.get(id)
    if(planet is None):
        return jsonify("planet not found"), 404
    
    return jsonify(planet.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
