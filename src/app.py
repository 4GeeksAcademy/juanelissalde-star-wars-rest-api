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
from models import db, User
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

@app.route('/user', methods=['GET'])
def handle_hello():


# @app.route('/todos', methods=['POST'])
# def add_new_todo():
#     request_body = request.get_json()  # Use get_json() to parse the JSON body
#     print("Incoming request with the following body", request_body)
#     todos.append(request_body)  # Add the new todo to the list
#     return jsonify(todos)  # Return the updated list

# @app.route('/todos/<int:position>', methods=['DELETE'])
# def delete_todo(position):
#     # Check if the position is valid
#     if position < 0 or position >= len(todos):
#         return jsonify({"error": "Invalid position"}), 400
#     del todos[position]
#     return jsonify(todos)

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
