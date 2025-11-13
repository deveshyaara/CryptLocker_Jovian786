#!/bin/bash

# Startup script for CryptLocker Web Wallet (Development)

echo "🚀 Starting CryptLocker Web Wallet Development Server..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18 or higher is required. Current version: $(node -v)"
    exit 1
fi

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "⚠️  .env.local not found. Copying from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env.local
        echo "✅ Created .env.local from template"
        echo "📝 Please update the API URLs in .env.local if needed"
    else
        echo "❌ .env.example not found. Creating default .env.local..."
        cat > .env.local << EOF
NEXT_PUBLIC_HOLDER_API_URL=http://localhost:8031
NEXT_PUBLIC_ISSUER_API_URL=http://localhost:8030
NEXT_PUBLIC_VERIFIER_API_URL=http://localhost:8032
NEXT_PUBLIC_API_URL=http://localhost:8031
NEXT_PUBLIC_WS_URL=ws://localhost:8031
EOF
        echo "✅ Created default .env.local"
    fi
fi

# Check if node_modules exists
if [ ! -d node_modules ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
fi

# Start development server
echo "🌐 Starting development server on http://localhost:3000..."
echo "⏳ This may take a moment..."
npm run dev
