#!/bin/bash

# Final System Check Script
# Quick validation before deployment

echo "╔════════════════════════════════════════════════════════╗"
echo "║    CRYPTLOCKER SYSTEM PRE-DEPLOYMENT CHECK           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

PASSED=0
FAILED=0

# Function to check status
check() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
        ((PASSED++))
    else
        echo "❌ $1"
        ((FAILED++))
    fi
}

# Check Python installation
python3 --version > /dev/null 2>&1
check "Python 3 installed"

# Check Docker installation
docker --version > /dev/null 2>&1
check "Docker installed"

docker-compose --version > /dev/null 2>&1
check "Docker Compose installed"

# Check file structure
[ -f "agents/issuer/app.py" ]
check "Issuer Agent files present"

[ -f "agents/verifier/app.py" ]
check "Verifier Agent files present"

[ -f "shared/services/ipfs_service.py" ]
check "IPFS Service present"

[ -f "infrastructure/docker-compose.yml" ]
check "Docker Compose config present"

[ -f "infrastructure/postgres/init.sql" ]
check "PostgreSQL schema present"

# Check Python imports
python3 -c "import sys; sys.path.insert(0, '.'); from agents.issuer.services.did_service import DIDService" > /dev/null 2>&1
check "Python imports work"

# Check Docker Compose config
cd infrastructure && docker-compose config --quiet > /dev/null 2>&1
check "Docker Compose config valid"
cd ..

# Check scripts are executable
[ -x "infrastructure/scripts/start-system.sh" ]
check "Start script executable"

[ -x "infrastructure/scripts/stop-system.sh" ]
check "Stop script executable"

# Check test files
[ -f "tests/test_issuer.py" ]
check "Test files present"

# Check documentation
[ -f "QUICKSTART_GUIDE.md" ]
check "Documentation present"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                   RESULTS                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "  ✅ Passed: $PASSED"
echo "  ❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 ALL CHECKS PASSED!"
    echo ""
    echo "System is ready for deployment."
    echo ""
    echo "Next steps:"
    echo "  1. Start services: bash infrastructure/scripts/start-system.sh"
    echo "  2. Wait ~30 seconds for initialization"
    echo "  3. Test: curl http://localhost:8000/health"
    echo "  4. Access docs: http://localhost:8000/docs"
    echo ""
    exit 0
else
    echo "⚠️  Some checks failed. Please review above."
    echo ""
    exit 1
fi
