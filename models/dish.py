from sqlalchemy import Column, Integer, String
from database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(String(255), primary_key=True)
    dish_name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    category = Column(Integer, nullable=False)
    photo = Column(String(255))
    ccal = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    fat = Column(Integer, nullable=False)
    carbohydrates = Column(Integer, nullable=False)

    def __init__(self, dish_name, description, price, category, available, photo, ccal, protein, fat, carbohydrates):
        self.dish_name = dish_name
        self.description = description
        self.price = price
        self.category = category
        self.available = available
        self.photo = photo
        self.ccal = ccal
        self.protein = protein
        self.fat = fat
        self.carbohydrates = carbohydrates
