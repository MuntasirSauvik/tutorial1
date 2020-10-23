import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from .meta import Base


class Message(Base):
    """ The SQLAlchemy declarative model class for a Message object. """
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message_text = Column(Text, nullable=True)
    dateTime = Column(DateTime, default=datetime.datetime.utcnow)

    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_messages')

    room_id = Column(Integer, ForeignKey('chatrooms.id'), nullable=False)
    room = relationship('Chatroom', backref='created_messages_room')
