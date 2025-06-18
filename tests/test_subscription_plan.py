import pytest
from flask import json

def test_create_subscription_plan(client):
    data = {
        'name': 'Premium Plan',
        'description': 'Advanced subscription with all features'
    }
    response = client.post('/api/v1/subscription-plans', json=data)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['name'] == data['name']

def test_list_subscription_plans(client):
    response = client.get('/api/v1/subscription-plans')
    assert response.status_code == 200
    assert isinstance(response.json, list)