from src.models import SubscriptionPlanVariation
from src.database import db_session

class SubscriptionPlanVariationService:
    @staticmethod
    def create_variation(plan_id, name, price, billing_frequency):
        variation = SubscriptionPlanVariation(
            plan_id=plan_id, 
            name=name, 
            price=price, 
            billing_frequency=billing_frequency
        )
        with db_session() as session:
            session.add(variation)
            session.commit()
            session.refresh(variation)
        return variation