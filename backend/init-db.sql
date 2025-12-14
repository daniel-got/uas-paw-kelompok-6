-- Initialize database and users
-- This script will be executed when PostgreSQL container starts

-- Create users if they don't exist (PostgreSQL 15 compatible)
DO $$
BEGIN
  CREATE ROLE alembic_user WITH LOGIN PASSWORD '12345';
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
  CREATE ROLE app_prod_user WITH LOGIN PASSWORD '12345';
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Connect to the database
\c uas_pengweb

-- Grant permissions to alembic_user
GRANT USAGE, CREATE ON SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alembic_user;

-- Grant permissions to app_prod_user
GRANT USAGE, CREATE ON SCHEMA public TO app_prod_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_prod_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_prod_user;

-- Default privileges
ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_prod_user;

ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_prod_user;
