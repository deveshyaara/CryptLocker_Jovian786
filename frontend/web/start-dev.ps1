# Startup script for CryptLocker Web Wallet (Development) - Windows

Write-Host "🚀 Starting CryptLocker Web Wallet Development Server..." -ForegroundColor Green

# Check if Node.js is installed
try {
    $nodeVersion = node -v
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+ first." -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
Set-Location $PSScriptRoot

# Check if .env.local exists
if (-not (Test-Path .env.local)) {
    Write-Host "⚠️  .env.local not found. Copying from .env.example..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env.local
        Write-Host "✅ Created .env.local from template" -ForegroundColor Green
        Write-Host "📝 Please update the API URLs in .env.local if needed" -ForegroundColor Cyan
    } else {
        Write-Host "❌ .env.example not found. Creating default .env.local..." -ForegroundColor Yellow
        @"
NEXT_PUBLIC_HOLDER_API_URL=http://localhost:8031
NEXT_PUBLIC_ISSUER_API_URL=http://localhost:8030
NEXT_PUBLIC_VERIFIER_API_URL=http://localhost:8032
NEXT_PUBLIC_API_URL=http://localhost:8031
NEXT_PUBLIC_WS_URL=ws://localhost:8031
"@ | Out-File -FilePath .env.local -Encoding UTF8
        Write-Host "✅ Created default .env.local" -ForegroundColor Green
    }
}

# Check if node_modules exists
if (-not (Test-Path node_modules)) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
}

# Start development server
Write-Host "🌐 Starting development server on http://localhost:3000..." -ForegroundColor Cyan
Write-Host "⏳ This may take a moment..." -ForegroundColor Yellow
npm run dev
