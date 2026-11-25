from flask_login import UserMixin, AnonymousUserMixin
from extension import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

import uuid
from datetime import datetime, timezone


class User(UserMixin ,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    role = db.Column(db.String(100), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
     
    
    
    created_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    updated_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )


    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

