from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    town = Column(String(255))
    street = Column(String(255))
    house = Column(String(10))
    apt = Column(Integer)
    block = Column(Integer)
    floor = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))  # Связь с User

    # Определяем связь с пользователем (один ко многим)
    user = relationship('User', back_populates='addresses')
