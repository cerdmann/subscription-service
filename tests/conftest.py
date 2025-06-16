import pytest
import os
import sys

# Ensure src directory is in Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(project_root, 'src'))

@pytest.fixture
def db_connection():
    """Fixture for database connection"""
    from src.utilities.database import get_db_connection
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
