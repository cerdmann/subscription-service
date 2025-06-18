from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    variation_id = Column(Integer, ForeignKey('subscription_plan_variations.id'), nullable=False)
    customer_id = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    status = Column(String, nullable=False)
    plan = relationship('SubscriptionPlan', back_populates='subscriptions')
    variation = relationship('SubscriptionPlanVariation')