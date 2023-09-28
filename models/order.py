from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    dish = Column(String(255), ForeignKey('dish.id'), nullable=False)
    count = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

    def __init__(self, dish, count, order_id):
        self.dish = dish
        self.count = count
        self.order_id = order_id

        order_dishes = relationship('OrderDish', backref='order', lazy=True)
