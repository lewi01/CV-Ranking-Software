from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = 'true')
    firstName = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    personality_type = db.Column(db.String(150))
    skills = db.Column(db.String(255))
    experience_rating = db.Column(db.String(255))
    degree = db.Column(db.String(255))
    experience = db.Column(db.String(255))

    notes = db.relationship('Note')




class Note(db.Model):
    id = db.Column(db.Integer, primary_key= 'true')
    data = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default = func.now() )
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key='true')
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    jobs = db.relationship('Job', backref='company', lazy=True)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key= 'true')
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    skills_required = db.Column(db.String(150))
    personality_required = db.Column(db.String(150))
    education_required = db.Column(db.String(150))
    experience_required = db.Column(db.Integer)

    skills_contribution = db.Column(db.Integer)
    experience_contribution = db.Column(db.Integer)
    education_contribution = db.Column(db.Integer)
    personality_contribution = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))


class Application(db.Model):
    id = db.Column(db.Integer, primary_key= 'true')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    percentage_score_skills = db.Column(db.Integer)
    percentage_score_personality = db.Column(db.Integer)
    percentage_score_experience = db.Column(db.Integer)
    percentage_score_education = db.Column(db.Integer)
    overall_percentage = db.Column(db.Integer)

    
