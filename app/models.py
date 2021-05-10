from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy.orm import session
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    edited = db.Column(db.DateTime, onupdate=datetime.now)
    role = db.Column(db.String(20))
    classes = db.relationship("Student_Class", back_populates="user")

    __mapper_args__ = {
        'polymorphic_on': role,
    }

    def set_password(self, passwordInput):
        self.password = generate_password_hash(passwordInput)

    def check_password(self, passwordInput):
        return check_password_hash(self.password, passwordInput)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Student(User):
    __tablename__ = "students"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lecturers_name = db.Column(db.String, nullable=False)
    classes = db.relationship("Class_", backref="subjects",lazy=True)

    def to_json(self, status):        
        return [{
                "subject_name": self.name,
                "lecturer_name": self.lecturers_name},
                {"success": status}]

    # lecturers_id = db.Column(db.Integer, db.ForeignKey('lectr'))

class Class_(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    lesson = db.Column(db.Integer, nullable=False)
    lesson_start = db.Column(db.Integer, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    users = db.relationship("Student_Class", back_populates="classes")


class Student_Class(db.Model):
    __tablename__ = "student_class"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(
        "classes.id"), nullable=False)
    user = db.relationship("User", back_populates="classes")
    classes = db.relationship("Class_", back_populates="users")