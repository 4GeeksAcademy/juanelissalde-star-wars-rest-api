"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for  # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_swagger import swagger # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorites
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
    # CODE GOES HERE

# Obtener usuarios--------------------------------------------------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data_serialized = [user.serialize() for user in users]
    return jsonify(data_serialized), 200

# Obtener usuario unico por id -------------------------------------------------------------
@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user = User.query.filter_by(id = id).first()
    if user == None:
        return jsonify('User not found'), 404
    else:
        return jsonify(user.serialize()), 200
 
# Obtener  favoritos de usuario por id -----------------------------------------------------
@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):
    user = User.query.get(id)
    if not user:
        return jsonify('user not found'), 404
    else:
        return jsonify(user.get_user_favorites()), 200

# Obtener Personajes -----------------------------------------------------------------------
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    data_serialized = [character.serialize() for character in characters]
    return jsonify(data_serialized), 200

# Obtener Planetas -------------------------------------------------------------------------
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    data_serialized = [planet.serialize() for planet in planets]
    return jsonify(data_serialized), 200

# Obtener Vehicluos ------------------------------------------------------------------------
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    data_serialized = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(data_serialized), 200

# Obtener personaje unico por id -----------------------------------------------------------
@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character = Character.query.filter_by(id = id).first()
    if character == None:
        return jsonify('Character not found'), 404
    else:
        character_serialized = character.serialize()
        return jsonify(character_serialized), 200

# Obtener planeta unico por id -------------------------------------------------------------
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet = Planet.query.filter_by(id = id).first()
    if planet == None:
        return jsonify('Planet not found'), 404
    else:
        planet_serialized = planet.serialize()
        return jsonify(planet_serialized), 200

# Obtener vehiculo unico por id ------------------------------------------------------------
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_one_vehicle(id):
    vehicle = Vehicle.query.filter_by(id = id).first()
    if vehicle == None:
        return jsonify('vehicle not found'), 404
    else:
        vehicle_serialized = vehicle.serialize()
        return jsonify(vehicle_serialized), 200

# Crear nuevo personaje --------------------------------------------------------------------
@app.route('/character', methods=['POST'])
def post_character():
    character = request.get_json()
    if not isinstance(character['img'], str) or len(character['img'].strip()) == 0:
         return({'error':'"img" must be a string'}), 400
    if not isinstance(character['name'], str) or len(character['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(character['gender'], str) or len(character['gender'].strip()) == 0:
         return({'error':'"gender" must be a string'}), 400
    if not isinstance(character['eye_color'], str) or len(character['eye_color'].strip()) == 0:
         return({'error':'"eye_color" must be a string'}), 400
    character_created = Character(img=character['img'],name=character['name'],gender=character['gender'],eye_color=character['eye_color'])
    print(character_created)
    db.session.add(character_created)
    db.session.commit()
    return jsonify('Character created'), 200

# Crear nuevo planeta --------------------------------------------------------------------
@app.route('/planet', methods=['POST'])
def post_planet():
    planet = request.get_json()
    if not isinstance(planet['img'], str) or len(planet['img'].strip()) == 0:
         return({'error':'"img" must be a string'}), 400
    if not isinstance(planet['name'], str) or len(planet['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(planet['population'], str) or len(planet['population'].strip()) == 0:
         return({'error':'"population" must be a string'}), 400
    if not isinstance(planet['terrain'], str) or len(planet['terrain'].strip()) == 0:
         return({'error':'"terrain" must be a string'}), 400
    planet_created = Planet(img=planet['img'],name=planet['name'],population=planet['population'],terrain=planet['terrain'])
    print(planet_created)
    db.session.add(planet_created)
    db.session.commit()
    return jsonify('planet created'), 200

# Crear nuevo vehiculo --------------------------------------------------------------------
@app.route('/vehicle', methods=['POST'])
def post_vehicle():
    vehicle = request.get_json()
    if not isinstance(vehicle['img'], str) or len(vehicle['img'].strip()) == 0:
         return({'error':'"img" must be a string'}), 400
    if not isinstance(vehicle['name'], str) or len(vehicle['name'].strip()) == 0:
         return({'error':'"name" must be a string'}), 400
    if not isinstance(vehicle['model'], str) or len(vehicle['model'].strip()) == 0:
         return({'error':'"model" must be a string'}), 400
    if not isinstance(vehicle['size'], str) or len(vehicle['size'].strip()) == 0:
         return({'error':'"size" must be a string'}), 400
    vehicle_created = Vehicle(img=vehicle['img'],name=vehicle['name'],model=vehicle['model'],size=vehicle['size'])
    print(vehicle_created)
    db.session.add(vehicle_created)
    db.session.commit()
    return jsonify('vehicle created'), 200

# Agregar personaje a favoritos tomando como referencia el id de usuario y personaje -------
@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if not user or not character:
        return jsonify({'User or character not found'}), 404
    else:
        new_favorite_character = Favorites(user_id = user_id, character_id = character_id)
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify(new_favorite_character.serialize()), 200
    
# Agregar planeta a favoritos tomando como referencia el id de usuario y planeta -----------
@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({'User or planet not found'}), 404
    else:
        new_favorite_planet = Favorites(user_id = user_id, planet_id = planet_id)
        db.session.add(new_favorite_planet)
        db.session.commit()
        return jsonify(new_favorite_planet.serialize()), 200

# Agregar vehiculo a favoritos tomando como referencia el id de usuario y vehiculo ---------
@app.route('/favorite/user/<int:user_id>/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)
    if not user or not vehicle:
        return jsonify({'User or vehicle not found'}), 404
    else:
        new_favorite_vehicle = Favorites(user_id = user_id, vehicle_id = vehicle_id)
        db.session.add(new_favorite_vehicle)
        db.session.commit()
        return jsonify(new_favorite_vehicle.serialize()), 200

# Eliminar favorito especifico por id ------------------------------------------------------
@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_one_favorite(id):
    favorite = Favorites.query.filter_by(id=id).first()
    if not favorite:
        return jsonify('favorite not found'), 404
    else:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify('favorite deleted'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
