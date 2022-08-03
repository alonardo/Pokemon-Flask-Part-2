from app import db, login
from flask_login import UserMixin # Only for user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)

    # This should return a unique id string
    def __repr__(self):
        return f'<User: {self.email}> | {self.id}'
    
    # For humans
    def __str__(self):
        return f'<User: {self.email}> | {self.first_name} {self.last_name}>'
    
    # Salt & hases our password to protect it
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    # Compare user password to password provided in login
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon= data['icon']
    
    def get_icon(self):
        return f'https://avatars.dicebear.com/api/personas/{self.icon}.svg'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
