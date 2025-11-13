-- PostgreSQL Initialization Script
-- Creates databases and tables for SSI wallet storage

-- Note: PostgreSQL does not support CREATE DATABASE IF NOT EXISTS
-- These databases are created by wallet applications on first use

-- Connect to main database
\c wallet_db;

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Metadata table for credential tracking
CREATE TABLE IF NOT EXISTS credential_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    credential_id VARCHAR(255) UNIQUE NOT NULL,
    schema_id VARCHAR(255) NOT NULL,
    cred_def_id VARCHAR(255) NOT NULL,
    holder_did VARCHAR(255),
    issuer_did VARCHAR(255) NOT NULL,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    ipfs_cid VARCHAR(255),
    attributes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Connection tracking table
CREATE TABLE IF NOT EXISTS connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_id VARCHAR(255) UNIQUE NOT NULL,
    their_did VARCHAR(255),
    their_label VARCHAR(255),
    state VARCHAR(50) NOT NULL,
    role VARCHAR(50),
    invitation_key VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Presentation requests tracking
CREATE TABLE IF NOT EXISTS presentation_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    presentation_exchange_id VARCHAR(255) UNIQUE NOT NULL,
    connection_id VARCHAR(255) REFERENCES connections(connection_id),
    proof_request JSONB NOT NULL,
    presentation JSONB,
    verified BOOLEAN DEFAULT FALSE,
    state VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IPFS document storage metadata
CREATE TABLE IF NOT EXISTS ipfs_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cid VARCHAR(255) UNIQUE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_size BIGINT,
    mime_type VARCHAR(100),
    credential_id VARCHAR(255) REFERENCES credential_metadata(credential_id),
    uploaded_by VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Schema tracking
CREATE TABLE IF NOT EXISTS schemas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    schema_id VARCHAR(255) UNIQUE NOT NULL,
    schema_name VARCHAR(255) NOT NULL,
    schema_version VARCHAR(50) NOT NULL,
    attributes TEXT[] NOT NULL,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Credential definitions tracking
CREATE TABLE IF NOT EXISTS credential_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cred_def_id VARCHAR(255) UNIQUE NOT NULL,
    schema_id VARCHAR(255) REFERENCES schemas(schema_id),
    tag VARCHAR(100) DEFAULT 'default',
    support_revocation BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log for security tracking
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Revocation registry tracking
CREATE TABLE IF NOT EXISTS revocation_registries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rev_reg_id VARCHAR(255) UNIQUE NOT NULL,
    cred_def_id VARCHAR(255) REFERENCES credential_definitions(cred_def_id),
    max_cred_num INTEGER NOT NULL,
    current_index INTEGER DEFAULT 0,
    state VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_credential_metadata_holder ON credential_metadata(holder_did);
CREATE INDEX idx_credential_metadata_issuer ON credential_metadata(issuer_did);
CREATE INDEX idx_credential_metadata_schema ON credential_metadata(schema_id);
CREATE INDEX idx_connections_state ON connections(state);
CREATE INDEX idx_presentation_requests_connection ON presentation_requests(connection_id);
CREATE INDEX idx_ipfs_documents_credential ON ipfs_documents(credential_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(created_at);
CREATE INDEX idx_audit_log_event_type ON audit_log(event_type);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
CREATE TRIGGER update_credential_metadata_updated_at
    BEFORE UPDATE ON credential_metadata
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_connections_updated_at
    BEFORE UPDATE ON connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_presentation_requests_updated_at
    BEFORE UPDATE ON presentation_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_revocation_registries_updated_at
    BEFORE UPDATE ON revocation_registries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Insert initial audit log entry
INSERT INTO audit_log (event_type, agent_type, details) 
VALUES ('database_initialized', 'system', '{"message": "Database initialized successfully"}');

COMMIT;
