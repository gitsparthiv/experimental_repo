from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Profile fields
    name = db.Column(db.String(150), default='Guest')
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(300), nullable=True)

    # Health Info
    blood_group = db.Column(db.String(10), nullable=True)
    blood_pressure = db.Column(db.String(50), nullable=True)

    # Preferences
    language = db.Column(db.String(50), default='English')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
            "address": self.address,
            "blood_group": self.blood_group,
            "blood_pressure": self.blood_pressure,
            "language": self.language
        }
