from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    status = db.Column(db.String(50)) # pending, active, inactive
    account_type=db.Column(db.String(50)) # student, mentor, admin
    availabilities = db.relationship('Availability')


class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(50))
    date = db.Column(db.String(150))  # YYYY-MM-DD
    start_time = db.Column(db.String(150))  # YYYY-MM-DDTHH:MM:SS
    end_time = db.Column(db.String(150))  # YYYY-MM-DDTHH:MM:SS
    # appointments = db.relationship('Appointment', back_populates='availability')
    appointments = db.relationship(
        'Appointment', 
        back_populates='availability', 
        cascade='all, delete-orphan'
    )

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(50))
    appointment_date = db.Column(db.String(150))  # YYYY-MM-DD
    start_time = db.Column(db.String(150))  # YYYY-MM-DDTHH:MM:SS
    end_time = db.Column(db.String(150))  # YYYY-MM-DDTHH:MM:SS
    status = db.Column(db.String(50))  # posted, booked, cancelled
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'))
    availability = db.relationship('Availability', back_populates='appointments')