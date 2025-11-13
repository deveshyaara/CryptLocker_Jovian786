#!/bin/bash

# Complete System Shutdown Script

set -e

echo "=========================================="
echo "Stopping SSI System"
echo "=========================================="

# Stop Docker services
echo "Stopping Docker services..."
cd infrastructure
docker-compose down

# Stop Indy network
echo "Stopping Indy network..."
bash scripts/stop-indy-network.sh

echo ""
echo "=========================================="
echo "All services stopped successfully!"
echo "=========================================="
