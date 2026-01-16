from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# User Model (UNCHANGED LOGIC)
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Profile fields
    name = db.Column(db.String(150), default="Guest")
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(300), nullable=True)

    # Health Info
    blood_group = db.Column(db.String(10), nullable=True)
    blood_pressure = db.Column(db.String(50), nullable=True)

    # Preferences
    language = db.Column(db.String(50), default="English")

    # ---------------------
    # Auth helpers
    # ---------------------
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
            "language": self.language,
        }


# =========================
# Hospital Model (NEW)
# =========================
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    distance = db.Column(db.String(50), nullable=True)
    doctors = db.Column(db.Integer, nullable=True)
    beds = db.Column(db.String(100), nullable=True)
    ventilators = db.Column(db.String(100), nullable=True)
    blood = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "name": self.name,
            "distance": self.distance,
            "doctors": self.doctors,
            "beds": self.beds,
            "ventilators": self.ventilators,
            "blood": self.blood,
        }


# =========================
# Seed Data (OPTIONAL, SAFE)
# =========================
def seed_hospitals():
    """
    Seed hospital data only if table is empty.
    Safe to call multiple times.
    """
    if Hospital.query.first():
        return

    hospitals = [
        Hospital(
            name="City General Hospital",
            distance="0.8 km",
            doctors=45,
            beds="120 (ICU: 25, Emergency: 30)",
            ventilators="15 (Available)",
            blood="Full Stock",
        ),
        Hospital(
            name="Metro Medical Center",
            distance="1.2 km",
            doctors=62,
            beds="180 (ICU: 35, Emergency: 45)",
            ventilators="22 (Available)",
            blood="Limited Stock",
        ),
        Hospital(
            name="Regional Health Institute",
            distance="2.1 km",
            doctors=38,
            beds="95 (ICU: 18, Emergency: 20)",
            ventilators="12 (Available)",
            blood="Full Stock",
        ),
    ]

    db.session.add_all(hospitals)
    db.session.commit()
