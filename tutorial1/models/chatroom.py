from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Boolean,
)

from .meta import Base


class Chatroom(Base):
    """ The SQLAlchemy declarative model class for a Chatroom object. """
    __tablename__ = 'chatrooms'
    id = Column(Integer, primary_key=True)
    roomDescription = Column(String(64), nullable=False, unique=True)
    door = Column(Boolean, nullable=True, default=True)
