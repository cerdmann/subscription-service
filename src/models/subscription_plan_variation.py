from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SubscriptionPlanVariation(Base):
    __tablename__ = 'subscription_plan_variations'

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    billing_frequency = Column(String, nullable=False)
    plan = relationship('SubscriptionPlan', back_populates='variations')