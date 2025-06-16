# Subscription Management System

## Overview
A comprehensive subscription management system built with Python and PostgreSQL.

## Features
- Create subscription plans
- Manage plan variations
- Track customer subscriptions
- Robust error handling
- Structured logging

## Prerequisites
- Python 3.9+
- PostgreSQL 13+

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/subscription-management.git
cd subscription-management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://username:password@localhost:5432/subscription_management
PORT=8000
LOG_LEVEL=INFO
```

## Running Tests
```bash
pytest tests/
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request