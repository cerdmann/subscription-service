from datetime import datetime
from src.models import Subscription
from src.database import db_session

class SubscriptionService:
    @staticmethod
    def create_subscription(plan_id, variation_id, customer_id):
        subscription = Subscription(
            plan_id=plan_id,
            variation_id=variation_id,
            customer_id=customer_id,
            start_date=datetime.utcnow(),
            status='active'
        )
        with db_session() as session:
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
        return subscription