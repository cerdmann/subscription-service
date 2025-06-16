from typing import Dict, Any, List

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__('; '.join(errors))

    def to_dict(self):
        return {
            'message': 'Validation Failed',
            'errors': self.errors
        }

def validate_subscription_plan(plan_data: Dict[str, Any]):
    """Validate subscription plan input"""
    errors = []

    # Name validation
    name = plan_data.get('name', '').strip()
    if not name or len(name) < 3 or len(name) > 255:
        errors.append('Name must be between 3 and 255 characters')

    # Description validation
    description = plan_data.get('description', '').strip()
    if not description or len(description) < 10 or len(description) > 500:
        errors.append('Description must be between 10 and 500 characters')

    # Category validation
    category = plan_data.get('category', '').strip()
    if not category or len(category) > 100:
        errors.append('Category is required and must be less than 100 characters')

    # Type validation
    valid_types = ['recurring', 'one-time', 'usage-based']
    plan_type = plan_data.get('type', '').lower()
    if plan_type not in valid_types:
        errors.append(f'Invalid subscription type. Must be one of: {", ".join(valid_types)}')

    if errors:
        raise ValidationError(errors)