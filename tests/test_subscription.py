def test_create_subscription(client):
    # First create a plan
    plan_data = {
        'name': 'Test Plan',
        'description': 'Test Plan Description'
    }
    plan_response = client.post('/api/v1/subscription-plans', json=plan_data)
    plan_id = plan_response.json['id']

    # Then create a variation
    variation_data = {
        'name': 'Monthly Variation',
        'price': 49.99,
        'billing_frequency': 'monthly'
    }
    variation_response = client.post(f'/api/v1/subscription-plans/{plan_id}/variations', json=variation_data)
    variation_id = variation_response.json['id']

    # Create subscription
    subscription_data = {
        'plan_id': plan_id,
        'variation_id': variation_id,
        'customer_id': 'test_customer_123'
    }
    response = client.post('/api/v1/subscriptions', json=subscription_data)
    
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['customer_id'] == 'test_customer_123'