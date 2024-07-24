from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship('Favorites', backref='favorites_user_id', lazy=True)
    
    def __repr__(self):
        return f'Email: {self.email} - ID: {self.id}'
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return f"User: {str(self.user_id)}{' - Character: ' + str(self.character_id) if self.character_id else ''}{' - Planet: ' + str(self.planet_id) if self.planet_id else ''}{' - Vehicle: ' + str(self.vehicle_id) if self.vehicle_id else ''}"
    def serialize(self):
        return {
            "id": self.id,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    gender = db.Column(db.String(40))
    eye = db.Column(db.String(20))

    favorites = db.relationship('Favorites', backref='favorites_character_id', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    population = db.Column(db.Integer)
    eye = db.Column(db.String(20))

    favorites = db.relationship('Favorites', backref='favorites_planet_id', lazy=True)


    def __repr__(self):
        return '<Planet %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    model = db.Column(db.String(40))
    size = db.Column(db.Integer)

    favorites = db.relationship('Favorites', backref='favorites_vehicle_id', lazy=True)


    def __repr__(self):
        return '<Vehicle %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
        }