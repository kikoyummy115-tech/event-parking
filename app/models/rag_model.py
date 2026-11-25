from extension import db
import uuid
from datetime import datetime, timezone


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(500), nullable=True)
    content_hash = db.Column(db.String(64), nullable=False)
    
    
    document_chunks = db.relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    
    created_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    



class DocumentChunk(db.Model):
    __tablename__ = "document_chunks"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_index = db.Column(db.Integer, nullable=False)

    content = db.Column(
        db.Text,
        nullable=False
    )
    
    embedding = db.Column(
        db.JSON,
        nullable=False
    )
    document_id = db.Column(db.String(36), db.ForeignKey('documents.id', ondelete="CASCADE"), nullable=True, index=True)
    document = db.relationship("Document", back_populates="document_chunks")
    
    __table_args__ = (
            db.UniqueConstraint(
                "document_id",
                "chunk_index",
                name="unique_document_chunk"
            ),
        )
    

class Conversation(db.Model):
    __tablename__ = "conversations"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    title = db.Column(
        db.String(255),
        nullable=True
    )    
    
    user_id = db.Column(db.String(36), nullable=True)
    
    
    messages = db.relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )

    
    created_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    



class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
       
    conversation_id = db.Column(
        db.String(36),
        db.ForeignKey("conversations.id"),
        nullable=False,
        index=True
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    conversation = db.relationship(
        "Conversation",
        back_populates="messages"
    )
    
