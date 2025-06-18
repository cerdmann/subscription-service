from flask import Blueprint, request, jsonify
from src.services import SubscriptionPlanService

subscription_plan_bp = Blueprint('subscription_plans', __name__)

@subscription_plan_bp.route('/subscription-plans', methods=['POST'])
def create_subscription_plan():
    data = request.json
    plan = SubscriptionPlanService.create_plan(
        name=data['name'], 
        description=data.get('description')
    )
    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'description': plan.description
    }), 201

@subscription_plan_bp.route('/subscription-plans', methods=['GET'])
def list_subscription_plans():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    plans = SubscriptionPlanService.list_plans(page, limit)
    return jsonify([
        {
            'id': plan.id,
            'name': plan.name,
            'description': plan.description
        } for plan in plans
    ])