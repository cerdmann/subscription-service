import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_db_connection(connection_string: str = None):
    """Create a database connection string"""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/subscription_management_test",
    )
