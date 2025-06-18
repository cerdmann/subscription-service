from datetime import datetime
from src.models import SubscriptionPlan
from src.database import db_session

class SubscriptionPlanService:
    @staticmethod
    def create_plan(name, description):
        plan = SubscriptionPlan(name=name, description=description, created_at=datetime.utcnow())
        with db_session() as session:
            session.add(plan)
            session.commit()
            session.refresh(plan)
        return plan

    @staticmethod
    def list_plans(page=1, limit=10):
        with db_session() as session:
            plans = session.query(SubscriptionPlan).offset((page-1)*limit).limit(limit).all()
            return plans