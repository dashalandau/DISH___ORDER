from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class OrderDish(Base):
    __tablename__ = 'order_dishes'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    address = Column(String(255), ForeignKey('address.id'), nullable=False)
    price = Column(Integer, nullable=False)
    ccal = Column(Integer, nullable=False)
    protein = Column(Integer, nullable=False)
    fat = Column(Integer, nullable=False)
    carb = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    order_date = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    status = Column(Integer, default=0, nullable=False)

    def __init__(self, user, address, price, ccal, protein, fat, carb, comment, order_date, rate, status):
        self.user = user
        self.address = address
        self.price = price
        self.ccal = ccal
        self.protein = protein
        self.fat = fat
        self.carb = carb
        self.comment = comment
        self.order_date = order_date
        self.rate = rate
        self.status = status


