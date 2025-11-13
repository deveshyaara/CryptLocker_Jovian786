#!/bin/bash

# Stop Indy Network

set -e

echo "Stopping Indy network..."

cd infrastructure/von-network
./manage stop

echo "Indy network stopped successfully!"
