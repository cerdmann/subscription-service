import pytest
from unittest.mock import Mock, patch
import psycopg2

from src.services.subscription_service import SubscriptionService
from src.utilities.validation import ValidationError

class MockConnection:
    def __init__(self, cursor_returns=None):
        self.cursor_returns = cursor_returns or []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def cursor(self, cursor_factory=None):
        return MockCursor(self.cursor_returns)

class MockCursor:
    def __init__(self, returns=None):
        self.returns = returns or []
        self.return_index = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetchone(self):
        if self.return_index < len(self.returns):
            result = self.returns[self.return_index]
            self.return_index += 1
            return result
        return None

    def execute(self, *args, **kwargs):
        pass

def test_create_subscription_plan_success():
    valid_plan_data = {
        'name': 'Monthly Coffee Subscription',
        'description': 'Receive premium coffee beans every month',
        'category': 'Food & Beverage',
        'type': 'recurring'
    }

    # Mock connection with predefined cursor behavior
    mock_connection = MockConnection(cursor_returns=[
        None,  # No existing plan
        {'id': 'test-plan-id', **valid_plan_data}  # Created plan
    ])

    # Patch psycopg2.connect to return our mock connection
    with patch('psycopg2.connect', return_value=mock_connection):
        # Create service and call method
        subscription_service = SubscriptionService()
        result = subscription_service.create_subscription_plan(valid_plan_data)

        # Assertions
        assert result['name'] == valid_plan_data['name']
        assert result['id'] == 'test-plan-id'

def test_create_subscription_plan_duplicate():
    duplicate_plan_data = {
        'name': 'Existing Coffee Subscription',
        'description': 'A plan that already exists',
        'category': 'Food & Beverage',
        'type': 'recurring'
    }

    # Mock connection with predefined cursor behavior
    mock_connection = MockConnection(cursor_returns=[
        {'id': 'existing-plan-id'}  # Existing plan
    ])

    # Patch psycopg2.connect to return our mock connection
    with patch('psycopg2.connect', return_value=mock_connection):
        # Create service and call method
        subscription_service = SubscriptionService()
        
        # Expect a ValidationError for duplicate plan
        with pytest.raises(ValidationError, match="A plan with this name already exists"):
            subscription_service.create_subscription_plan(duplicate_plan_data)

def test_create_subscription_plan_validation_error():
    subscription_service = SubscriptionService()
    
    invalid_plans = [
        {'name': '', 'description': 'Test Description', 'category': 'Test', 'type': 'recurring'},
        {'name': 'Valid Name', 'description': '', 'category': 'Test', 'type': 'recurring'},
        {'name': 'Valid Name', 'description': 'Valid Description', 'category': '', 'type': 'recurring'},
        {'name': 'Valid Name', 'description': 'Valid Description', 'category': 'Test', 'type': 'invalid-type'}
    ]

    for invalid_plan in invalid_plans:
        with pytest.raises(ValidationError):
            subscription_service.create_subscription_plan(invalid_plan)