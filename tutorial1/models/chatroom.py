from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
)

from .meta import Base


class Chatroom(Base):
    """ The SQLAlchemy declarative model class for a Chatroom object. """
    __tablename__ = 'chatrooms'
    id = Column(Integer, primary_key=True)
    roomNumber = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    door = Column(Boolean, nullable=True)
