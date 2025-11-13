#!/bin/bash

# Indy Network Setup Script
# Deploys a 4-node Hyperledger Indy test network using von-network

set -e

echo "=========================================="
echo "Indy Network Setup"
echo "=========================================="

# Clone von-network if not exists
if [ ! -d "infrastructure/von-network" ]; then
    echo "Cloning von-network repository..."
    cd infrastructure
    git clone https://github.com/bcgov/von-network.git
    cd ..
fi

cd infrastructure/von-network

# Build von-network
echo "Building von-network Docker images..."
./manage build

# Start the network
echo "Starting 4-node Indy network..."
./manage start --logs

echo ""
echo "=========================================="
echo "Indy Network Started Successfully!"
echo "=========================================="
echo ""
echo "Ledger Browser: http://localhost:9000"
echo "Genesis File: http://localhost:9000/genesis"
echo ""
echo "Node endpoints:"
echo "  - Node1: localhost:9701"
echo "  - Node2: localhost:9703"
echo "  - Node3: localhost:9705"
echo "  - Node4: localhost:9707"
echo ""
echo "To stop the network: cd infrastructure/von-network && ./manage stop"
echo "=========================================="
