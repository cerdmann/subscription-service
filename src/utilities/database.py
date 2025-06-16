import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection(connection_string: str = None):
    """Create a database connection"""
    if not connection_string:
        connection_string = os.getenv('DATABASE_URL', 
            'postgresql://username:password@localhost:5432/subscription_management')
    
    try:
        conn = psycopg2.connect(connection_string)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise