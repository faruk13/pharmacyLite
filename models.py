import datetime
from App import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from App import login
from datetime import date

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email= db.Column(db.String(128), index=True, unique=True)
    password_hash=db.Column(db.String(128))

    def __repr__(self): ##user for debugging purposes
        return '< User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
  
    def get_id(self):
        return (self.userId)

class Manuf(db.Model):
    manufId=db.Column(db.Integer, primary_key=True)
    manufName=db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Manuf {}>'.format(self.manufName)

class MedStock(db.Model):
    medId=db.Column(db.Integer, primary_key=True)
    medName=db.Column(db.String(120), index=True, unique=True)
    manufId=db.Column(db.Integer, db.ForeignKey(Manuf.manufId))
    manufName=db.Column(db.String(120), db.ForeignKey(Manuf.manufName))
    availQnty=db.Column(db.Integer)
    CO1=db.Column(db.Integer) # cost of 1
    expDate=db.Column(db.Date )

    def __repr__(self):
        return '<MedStock {}>'.format(self.medName)

class ManufStock(db.Model):
    mStockid=db.Column(db.Integer, primary_key=True)
    manufId=db.Column(db.Integer, db.ForeignKey(Manuf.manufId), unique=False)
    availMedId=db.Column(db.Integer, db.ForeignKey(MedStock.medId), unique=False)
    availMedName=db.Column(db.String(120), db.ForeignKey(MedStock.medName), unique=False)
    availManufQnty=db.Column(db.Integer)

    def __repr__(self):
        return '<ManufStock {}>'.format(self.availMedName)



class BoughtBy(db.Model):
    cusId= db.Column(db.Integer, primary_key=True)
    cusName= db.Column(db.String(120), index=True, unique=True)
    medId= db.Column(db.Integer, db.ForeignKey(MedStock.medId))
    buyQnty= db.Column(db.Integer)
    date= db.Column(db.Date, default=date.today())
    CO1=db.Column(db.Integer,  db.ForeignKey(MedStock.CO1))
    totCost=buyQnty*CO1

    def __repr__(self):
        return '<BoughtBy {}>'.format(self.cusName)


class OrderMedFor(db.Model):
    orderId= db.Column(db.Integer, primary_key=True)
    medId= db.Column(db.Integer, db.ForeignKey(MedStock.medId))
    medName= db.Column(db.String(120), db.ForeignKey(MedStock.medName)) 
    toManufId=db.Column(db.Integer,  db.ForeignKey(Manuf.manufId))
    wantQnty= db.Column(db.Integer)
    byDate=db.Column(db.Date )

    def __repr__(self):
        return '<OrderMedFor {}>'.format(self.medName)

