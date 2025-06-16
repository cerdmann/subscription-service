import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_schema(connection_string: str):
    """Create database schema with all necessary tables"""
    ddl_script = """
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Subscription Plans Table
    CREATE TABLE IF NOT EXISTS subscription_plans (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT NOT NULL,
        category VARCHAR(100) NOT NULL,
        type VARCHAR(50) NOT NULL DEFAULT 'recurring',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT TRUE
    );

    -- Subscription Plan Variations Table
    CREATE TABLE IF NOT EXISTS subscription_plan_variations (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        plan_id UUID REFERENCES subscription_plans(id),
        name VARCHAR(255) NOT NULL,
        billing_interval VARCHAR(50) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        currency VARCHAR(10) NOT NULL DEFAULT 'USD',
        trial_period_days INTEGER DEFAULT 0,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT TRUE
    );

    -- Customers Table
    CREATE TABLE IF NOT EXISTS customers (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        email VARCHAR(255) NOT NULL UNIQUE,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        phone_number VARCHAR(20),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        last_active_at TIMESTAMP WITH TIME ZONE
    );

    -- Subscriptions Table
    CREATE TABLE IF NOT EXISTS subscriptions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        customer_id UUID REFERENCES customers(id),
        plan_variation_id UUID REFERENCES subscription_plan_variations(id),
        status VARCHAR(50) NOT NULL DEFAULT 'active',
        start_date DATE NOT NULL,
        next_billing_date DATE,
        current_period_start DATE,
        current_period_end DATE,
        cancel_at_period_end BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- Billing Transactions Table
    CREATE TABLE IF NOT EXISTS billing_transactions (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        subscription_id UUID REFERENCES subscriptions(id),
        amount NUMERIC(10, 2) NOT NULL,
        currency VARCHAR(10) NOT NULL DEFAULT 'USD',
        status VARCHAR(50) NOT NULL,
        transaction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        payment_method VARCHAR(100),
        invoice_number VARCHAR(100)
    );

    -- Performance Indexes
    CREATE INDEX IF NOT EXISTS idx_subscriptions_customer_id ON subscriptions(customer_id);
    CREATE INDEX IF NOT EXISTS idx_subscriptions_plan_variation_id ON subscriptions(plan_variation_id);
    CREATE INDEX IF NOT EXISTS idx_billing_transactions_subscription_id ON billing_transactions(subscription_id);
    """

    try:
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        db_name = os.environ["POSTGRES_DB"]
        # Establish connection
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host="localhost",
            port="5432",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create cursor
        with conn.cursor() as cur:
            # Execute the DDL script
            cur.execute(ddl_script)

        print("Database schema created successfully")

    except psycopg2.Error as e:
        print(f"Error creating database schema: {e}")
        raise
    finally:
        if conn:
            conn.close()


def drop_database_schema(connection_string: str):
    """Drop all tables in the schema (use with caution)"""
    drop_script = """
    DROP TABLE IF EXISTS billing_transactions;
    DROP TABLE IF EXISTS subscriptions;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS subscription_plan_variations;
    DROP TABLE IF EXISTS subscription_plans;
    DROP EXTENSION IF EXISTS "uuid-ossp";
    """

    try:
        # Establish connection
        conn = psycopg2.connect(connection_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create cursor
        with conn.cursor() as cur:
            # Execute the drop script
            cur.execute(drop_script)

        print("Database schema dropped successfully")

    except psycopg2.Error as e:
        print(f"Error dropping database schema: {e}")
        raise
    finally:
        if conn:
            conn.close()
