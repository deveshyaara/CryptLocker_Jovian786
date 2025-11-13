-- Holder Agent Database Schema
-- Creates tables for user management and credential storage

-- Users table for holder authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    did VARCHAR(255),
    wallet_id VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast username lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_did ON users(did);

-- Credential storage table for holder credentials
CREATE TABLE IF NOT EXISTS credential_storage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    credential_id VARCHAR(255) UNIQUE NOT NULL,
    schema_id VARCHAR(255),
    cred_def_id VARCHAR(255),
    attributes JSONB NOT NULL,
    ipfs_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast credential lookups
CREATE INDEX IF NOT EXISTS idx_credential_storage_user_id ON credential_storage(user_id);
CREATE INDEX IF NOT EXISTS idx_credential_storage_credential_id ON credential_storage(credential_id);
CREATE INDEX IF NOT EXISTS idx_credential_storage_schema_id ON credential_storage(schema_id);

-- Connection tracking table (optional - for audit)
CREATE TABLE IF NOT EXISTS connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    connection_id VARCHAR(255) UNIQUE NOT NULL,
    their_did VARCHAR(255),
    their_label VARCHAR(255),
    state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for connection lookups
CREATE INDEX IF NOT EXISTS idx_connections_user_id ON connections(user_id);
CREATE INDEX IF NOT EXISTS idx_connections_connection_id ON connections(connection_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to auto-update updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_credential_storage_updated_at ON credential_storage;
CREATE TRIGGER update_credential_storage_updated_at
    BEFORE UPDATE ON credential_storage
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_connections_updated_at ON connections;
CREATE TRIGGER update_connections_updated_at
    BEFORE UPDATE ON connections
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample user (for testing only - remove in production)
-- Password: test123 (hashed with bcrypt)
INSERT INTO users (username, email, full_name, hashed_password)
VALUES ('testuser', 'test@example.com', 'Test User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIbXXXXXXX')
ON CONFLICT (username) DO NOTHING;

-- Grant permissions (adjust as needed)
-- These are handled by PostgreSQL container user settings
