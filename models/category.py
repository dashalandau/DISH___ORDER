from sqlalchemy import Column, Integer, String
from database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
