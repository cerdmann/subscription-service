from flask import Blueprint, request, jsonify
from src.services import SubscriptionPlanVariationService

subscription_plan_variation_bp = Blueprint('subscription_plan_variations', __name__)

@subscription_plan_variation_bp.route('/subscription-plans/<int:plan_id>/variations', methods=['POST'])
def create_plan_variation(plan_id):
    data = request.json
    variation = SubscriptionPlanVariationService.create_variation(
        plan_id=plan_id,
        name=data['name'],
        price=data['price'],
        billing_frequency=data['billing_frequency']
    )
    return jsonify({
        'id': variation.id,
        'plan_id': variation.plan_id,
        'name': variation.name,
        'price': variation.price,
        'billing_frequency': variation.billing_frequency
    }), 201