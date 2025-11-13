# Issuer Agent - ACA-Py Configuration
# Hyperledger Aries Cloud Agent for Credential Issuance

FROM ghcr.io/hyperledger/aries-cloudagent-python:py3.9-0.11.0

USER root

# Install additional dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.0 \
    uvicorn[standard]==0.24.0 \
    psycopg2-binary==2.9.9 \
    python-multipart==0.0.6 \
    aiohttp==3.9.0 \
    python-dotenv==1.0.0

# Disable uvloop to fix event loop issues
RUN pip uninstall -y uvloop || true

# Create application directory
WORKDIR /app

# Copy application code
COPY . /app/

# Set permissions
RUN chmod +x /app/scripts/*.sh || true

# Switch to aries user for security
USER aries

# Expose ports
EXPOSE 8020 8030

# Health check - check both agent admin API and FastAPI
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health 2>/dev/null || exit 1

# Entry point
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["aca-py start \
    --inbound-transport http 0.0.0.0 ${AGENT_PORT} \
    --outbound-transport http \
    --admin 0.0.0.0 ${ADMIN_PORT} \
    --admin-api-key ${ADMIN_API_KEY} \
    --wallet-type askar \
    --wallet-name ${WALLET_NAME} \
    --wallet-key ${WALLET_KEY} \
    --wallet-storage-type default \
    --genesis-url ${GENESIS_URL} \
    --seed ${PUBLIC_DID_SEED} \
    --endpoint http://issuer-agent:${AGENT_PORT} \
    --label \"${AGENT_NAME}\" \
    --public-invites \
    --auto-provision \
    --auto-ping-connection \
    --monitor-ping \
    --log-level ${LOG_LEVEL:-info}"]
