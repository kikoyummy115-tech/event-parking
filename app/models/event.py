import uuid
from extension import db
from  datetime import datetime, timezone



class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String(100), nullable=False, index=True)
    image_url = db.Column(db.Text, nullable=True)
    public_id = db.Column(db.Text, nullable=True)
    
    location = db.Column(db.String(100), nullable=False)
    location_link = db.Column(db.Text, nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    
    description = db.Column(db.Text, nullable=False)
    
    zones = db.relationship("Zone", back_populates="event", cascade="all, delete-orphan")
    
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
    

class Zone(db.Model):
    __tablename__ = "zones"
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String(100), nullable=False, index=True)
    vehicle = db.Column(db.String(100), nullable=False)
    
    
    location = db.Column(db.String(100), nullable=False)
    location_link = db.Column(db.Text, nullable=False)

    event_id = db.Column(db.String(36), db.ForeignKey('events.id', ondelete="CASCADE"), nullable=False, index=True)
    event = db.relationship("Event", back_populates="zones")
    
    
    
    
#### === Assumption for booking ==####

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    number_of_clicked = db.Column(db.Integer, nullable=True)
    
    