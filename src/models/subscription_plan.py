from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, nullable=False)
    variations = relationship('SubscriptionPlanVariation', back_populates='plan')
    subscriptions = relationship('Subscription', back_populates='plan')