from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    districts = db.relationship('District', backref='region', lazy=True)

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

class Quota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

class GOP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256))
    phone_number = db.Column(db.String(64))
    iin = db.Column(db.String(32))
    school = db.Column(db.String(256))
    score = db.Column(db.Integer)
    group = db.Column(db.String(64))        
    course = db.Column(db.Integer)         
    lang = db.Column(db.String(64))        

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    quota_id = db.Column(db.Integer, db.ForeignKey('quota.id'))
    gop_id = db.Column(db.Integer, db.ForeignKey('gop.id'))
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
