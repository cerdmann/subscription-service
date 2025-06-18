from flask import Blueprint, request, jsonify
from src.services import SubscriptionService

subscription_bp = Blueprint('subscriptions', __name__)

@subscription_bp.route('/subscriptions', methods=['POST'])
def create_subscription():
    data = request.json
    subscription = SubscriptionService.create_subscription(
        plan_id=data['plan_id'],
        variation_id=data['variation_id'],
        customer_id=data['customer_id']
    )
    return jsonify({
        'id': subscription.id,
        'plan_id': subscription.plan_id,
        'variation_id': subscription.variation_id,
        'customer_id': subscription.customer_id,
        'start_date': subscription.start_date.isoformat(),
        'status': subscription.status
    }), 201