from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telephone = Column(Integer, unique=True)
    email = Column(String(255))
    password = Column(String(255))
    tg_link = Column(String(255))
    type = Column(Integer, default=1)

    addresses = relationship('Address', back_populates='user')

    def __init__(self, telephone, email, password, tg_link, type):
        self.telephone = telephone
        self.email = email
        self.password = password
        self.tg_link = tg_link
        self.type = type


