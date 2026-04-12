import bcrypt
from database import db
from datetime import datetime

class User(db.Model): #create a model
    __tablename__ = 'users' #table name

    id = db.Column(db.Integer, primary_key=True) #primary key/ unique key so every user has a unique key. foreign_key = sleep id //primary kjey 
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sleep_entries = db.relationship('SleepEntry', #no dublicaiton
        backref='owner', lazy=True, cascade='all, delete-orphan')
    sleep_goal = db.relationship('SleepGoal',
        backref='owner', lazy=True, #save memory 
        uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt) #end conding map
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password. encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
