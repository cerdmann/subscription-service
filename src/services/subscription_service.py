import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List

import psycopg2
from psycopg2.extras import RealDictCursor

from src.utilities.validation import ValidationError, validate_subscription_plan
from src.utilities.logger import logger
from src.utilities.database import get_db_connection

class SubscriptionService:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or get_db_connection()

    def _sanitize_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input to prevent XSS and injection"""
        return {k: self._sanitize_value(v) for k, v in input_data.items()}

    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize individual input values"""
        if isinstance(value, str):
            return value.strip().replace('<', '').replace('>', '')
        return value

    def create_subscription_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new subscription plan"""
        try:
            # Validate input
            validate_subscription_plan(plan_data)

            # Sanitize input
            sanitized_data = self._sanitize_input(plan_data)

            # Generate unique plan ID
            plan_id = str(uuid.uuid4())

            with psycopg2.connect(self.connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Check for existing plan
                    cur.execute(
                        "SELECT id FROM subscription_plans WHERE name = %s", 
                        (sanitized_data['name'],)
                    )
                    if cur.fetchone():
                        raise ValidationError(["A plan with this name already exists"])

                    # Insert new plan
                    cur.execute(
                        """INSERT INTO subscription_plans 
                        (id, name, description, category, type) 
                        VALUES (%s, %s, %s, %s, %s) 
                        RETURNING *""",
                        (
                            plan_id, 
                            sanitized_data['name'], 
                            sanitized_data['description'], 
                            sanitized_data['category'], 
                            sanitized_data.get('type', 'recurring')
                        )
                    )
                    created_plan = cur.fetchone()

                    # Log successful creation
                    logger.info(
                        "Subscription plan created", 
                        extra={
                            "plan_id": created_plan['id'],
                            "plan_name": created_plan['name']
                        }
                    )

                    return created_plan

        except (ValidationError, psycopg2.Error) as e:
            # Log error
            logger.error(
                "Error creating subscription plan", 
                extra={
                    "error": str(e),
                    "plan_data": plan_data
                }
            )
            raise

    def create_plan_variation(self, plan_id: str, variation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a variation for an existing subscription plan"""
        try:
            # Validate input
            self._validate_plan_variation(variation_data)

            # Sanitize input
            sanitized_data = self._sanitize_input(variation_data)

            # Generate unique variation ID
            variation_id = str(uuid.uuid4())

            with psycopg2.connect(self.connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Verify plan exists
                    cur.execute("SELECT id FROM subscription_plans WHERE id = %s", (plan_id,))
                    if not cur.fetchone():
                        raise ValidationError(["Parent plan does not exist"])

                    # Insert plan variation
                    cur.execute(
                        """INSERT INTO subscription_plan_variations 
                        (id, plan_id, name, billing_interval, price, currency, trial_period_days) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        RETURNING *""",
                        (
                            variation_id,
                            plan_id,
                            sanitized_data['name'],
                            sanitized_data['billing_interval'],
                            sanitized_data['price'],
                            sanitized_data.get('currency', 'USD'),
                            sanitized_data.get('trial_period_days', 0)
                        )
                    )
                    created_variation = cur.fetchone()

                    # Log successful creation
                    logger.info(
                        "Plan variation created", 
                        extra={
                            "variation_id": created_variation['id'],
                            "plan_id": plan_id
                        }
                    )

                    return created_variation

        except (ValidationError, psycopg2.Error) as e:
            # Log error
            logger.error(
                "Error creating plan variation", 
                extra={
                    "error": str(e),
                    "plan_id": plan_id,
                    "variation_data": variation_data
                }
            )
            raise

    def _validate_plan_variation(self, variation_data: Dict[str, Any]):
        """Validate plan variation input"""
        errors = []

        # Name validation
        name = variation_data.get('name', '').strip()
        if not name or len(name) < 3 or len(name) > 255:
            errors.append('Variation name must be between 3 and 255 characters')

        # Price validation
        price = variation_data.get('price')
        if not isinstance(price, (int, float)) or price <= 0:
            errors.append('Price must be a positive number')

        # Billing interval validation
        valid_intervals = ['weekly', 'monthly', 'yearly']
        billing_interval = variation_data.get('billing_interval', '').lower()
        if billing_interval not in valid_intervals:
            errors.append(f'Invalid billing interval. Must be one of: {", ".join(valid_intervals)}')

        if errors:
            raise ValidationError(errors)

    def create_subscription(self, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer subscription"""
        try:
            # Validate input
            self._validate_subscription(subscription_data)

            # Sanitize input
            sanitized_data = self._sanitize_input(subscription_data)

            # Generate unique subscription ID
            subscription_id = str(uuid.uuid4())

            # Calculate billing dates
            start_date = datetime.strptime(sanitized_data['start_date'], '%Y-%m-%d')
            next_billing_date = self._calculate_next_billing_date(
                start_date, 
                sanitized_data['billing_interval']
            )

            with psycopg2.connect(self.connection_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Insert subscription
                    cur.execute(
                        """INSERT INTO subscriptions 
                        (id, customer_id, plan_variation_id, start_date, next_billing_date, 
                        current_period_start, current_period_end) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        RETURNING *""",
                        (
                            subscription_id,
                            sanitized_data['customer_id'],
                            sanitized_data['plan_variation_id'],
                            start_date,
                            next_billing_date,
                            start_date,
                            next_billing_date
                        )
                    )
                    created_subscription = cur.fetchone()

                    # Log successful creation
                    logger.info(
                        "Subscription created", 
                        extra={
                            "subscription_id": created_subscription['id'],
                            "customer_id": sanitized_data['customer_id']
                        }
                    )

                    return created_subscription

        except (ValidationError, psycopg2.Error) as e:
            # Log error
            logger.error(
                "Error creating subscription", 
                extra={
                    "error": str(e),
                    "subscription_data": subscription_data
                }
            )
            raise

    def _validate_subscription(self, subscription_data: Dict[str, Any]):
        """Validate subscription creation data"""
        errors = []

        # Customer ID validation
        if not subscription_data.get('customer_id'):
            errors.append("Customer ID is required")

        # Plan Variation ID validation
        if not subscription_data.get('plan_variation_id'):
            errors.append("Plan Variation ID is required")

        # Start Date validation
        try:
            datetime.strptime(subscription_data.get('start_date', ''), '%Y-%m-%d')
        except (ValueError, TypeError):
            errors.append("Invalid start date format. Use YYYY-MM-DD")

        # Billing Interval validation
        valid_intervals = ['weekly', 'monthly', 'yearly']
        if subscription_data.get('billing_interval') not in valid_intervals:
            errors.append(f"Invalid billing interval. Must be one of: {', '.join(valid_intervals)}")

        if errors:
            raise ValidationError(errors)

    def _calculate_next_billing_date(self, start_date: datetime, billing_interval: str) -> datetime:
        """Calculate the next billing date based on interval"""
        if billing_interval == 'weekly':
            return start_date + timedelta(weeks=1)
        elif billing_interval == 'monthly':
            return start_date + timedelta(days=30)
        elif billing_interval == 'yearly':
            return start_date + timedelta(days=365)
        else:
            raise ValueError("Invalid billing interval")