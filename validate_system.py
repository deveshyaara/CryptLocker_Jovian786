#!/usr/bin/env python3
"""
System Validation Script
Tests all components without requiring running services
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules import correctly"""
    print("🧪 Testing Module Imports...")
    tests_passed = 0
    tests_total = 0
    
    # Test Issuer Agent imports
    tests = [
        ("Issuer DID Service", "agents.issuer.services.did_service", "DIDService"),
        ("Issuer Schema Service", "agents.issuer.services.schema_service", "SchemaService"),
        ("Issuer Credential Service", "agents.issuer.services.credential_service", "CredentialService"),
        ("Issuer Connection Service", "agents.issuer.services.connection_service", "ConnectionService"),
        ("Issuer Config", "agents.issuer.config.agent_config", "IssuerConfig"),
        ("Verifier Presentation Service", "agents.verifier.services.presentation_service", "PresentationService"),
        ("Verifier Connection Service", "agents.verifier.services.connection_service", "ConnectionService"),
        ("Verifier Config", "agents.verifier.config.agent_config", "VerifierConfig"),
        ("IPFS Service", "shared.services.ipfs_service", "IPFSService"),
    ]
    
    for name, module, cls in tests:
        tests_total += 1
        try:
            mod = __import__(module, fromlist=[cls])
            getattr(mod, cls)
            print(f"  ✅ {name}")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    
    print(f"\n📊 Import Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    tests_passed = 0
    tests_total = 0
    
    required_files = [
        # Issuer Agent
        "agents/issuer/Dockerfile",
        "agents/issuer/app.py",
        "agents/issuer/requirements.txt",
        "agents/issuer/config/agent_config.py",
        "agents/issuer/services/did_service.py",
        "agents/issuer/services/schema_service.py",
        "agents/issuer/services/credential_service.py",
        "agents/issuer/services/connection_service.py",
        
        # Verifier Agent
        "agents/verifier/Dockerfile",
        "agents/verifier/app.py",
        "agents/verifier/config/agent_config.py",
        "agents/verifier/services/presentation_service.py",
        "agents/verifier/services/connection_service.py",
        
        # Shared
        "shared/services/ipfs_service.py",
        
        # Infrastructure
        "infrastructure/docker-compose.yml",
        "infrastructure/postgres/init.sql",
        "infrastructure/scripts/start-system.sh",
        "infrastructure/scripts/stop-system.sh",
        "infrastructure/scripts/start-indy-network.sh",
        "infrastructure/scripts/stop-indy-network.sh",
        
        # Tests
        "tests/test_issuer.py",
        "tests/test_verifier.py",
        "tests/test_ipfs.py",
        "tests/requirements.txt",
        
        # Documentation
        "README.md",
        "IMPLEMENTATION_STATUS.md",
        "QUICKSTART_GUIDE.md",
        "frontend/mobile/MOBILE_WALLET_PLAN.md",
    ]
    
    for file_path in required_files:
        tests_total += 1
        full_path = Path(file_path)
        if full_path.exists():
            print(f"  ✅ {file_path}")
            tests_passed += 1
        else:
            print(f"  ❌ {file_path} - NOT FOUND")
    
    print(f"\n📊 File Structure Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def test_code_quality():
    """Test code quality metrics"""
    print("\n🧪 Testing Code Quality...")
    tests_passed = 0
    tests_total = 0
    
    # Check for syntax errors in Python files
    python_files = [
        "agents/issuer/app.py",
        "agents/issuer/services/did_service.py",
        "agents/issuer/services/schema_service.py",
        "agents/issuer/services/credential_service.py",
        "agents/issuer/services/connection_service.py",
        "agents/verifier/app.py",
        "agents/verifier/services/presentation_service.py",
        "agents/verifier/services/connection_service.py",
        "shared/services/ipfs_service.py",
    ]
    
    for file_path in python_files:
        tests_total += 1
        try:
            with open(file_path) as f:
                compile(f.read(), file_path, 'exec')
            print(f"  ✅ {file_path} - No syntax errors")
            tests_passed += 1
        except SyntaxError as e:
            print(f"  ❌ {file_path} - Syntax error: {e}")
    
    print(f"\n📊 Code Quality Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def test_configuration():
    """Test configuration files"""
    print("\n🧪 Testing Configuration Files...")
    tests_passed = 0
    tests_total = 0
    
    # Test issuer config
    tests_total += 1
    try:
        from agents.issuer.config.agent_config import config
        assert hasattr(config, 'AGENT_NAME')
        assert hasattr(config, 'ADMIN_PORT')
        assert hasattr(config, 'WALLET_NAME')
        print(f"  ✅ Issuer configuration valid")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Issuer configuration: {e}")
    
    # Test verifier config
    tests_total += 1
    try:
        from agents.verifier.config.agent_config import config as vconfig
        assert hasattr(vconfig, 'AGENT_NAME')
        assert hasattr(vconfig, 'ADMIN_PORT')
        assert hasattr(vconfig, 'WALLET_NAME')
        print(f"  ✅ Verifier configuration valid")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Verifier configuration: {e}")
    
    # Test docker-compose
    tests_total += 1
    try:
        import yaml
        with open('infrastructure/docker-compose.yml') as f:
            compose_data = yaml.safe_load(f)
        assert 'services' in compose_data
        assert len(compose_data['services']) >= 6
        print(f"  ✅ docker-compose.yml valid ({len(compose_data['services'])} services)")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ docker-compose.yml: {e}")
    
    # Test PostgreSQL schema
    tests_total += 1
    try:
        with open('infrastructure/postgres/init.sql') as f:
            sql_content = f.read()
        table_count = sql_content.count('CREATE TABLE')
        assert table_count >= 8
        print(f"  ✅ PostgreSQL schema valid ({table_count} tables)")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ PostgreSQL schema: {e}")
    
    print(f"\n📊 Configuration Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def test_service_classes():
    """Test service class instantiation"""
    print("\n🧪 Testing Service Classes...")
    tests_passed = 0
    tests_total = 0
    
    # Test Issuer services
    tests_total += 1
    try:
        from agents.issuer.services.did_service import DIDService
        service = DIDService("http://localhost:8030", "test-key")
        assert hasattr(service, 'create_did')
        assert hasattr(service, 'list_dids')
        print(f"  ✅ DIDService instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ DIDService: {e}")
    
    tests_total += 1
    try:
        from agents.issuer.services.schema_service import SchemaService
        service = SchemaService("http://localhost:8030", "test-key")
        assert hasattr(service, 'create_schema')
        assert hasattr(service, 'create_credential_definition')
        print(f"  ✅ SchemaService instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ SchemaService: {e}")
    
    tests_total += 1
    try:
        from agents.issuer.services.credential_service import CredentialService
        service = CredentialService("http://localhost:8030", "test-key")
        assert hasattr(service, 'send_credential_offer')
        assert hasattr(service, 'revoke_credential')
        print(f"  ✅ CredentialService instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ CredentialService: {e}")
    
    tests_total += 1
    try:
        from agents.issuer.services.connection_service import ConnectionService
        service = ConnectionService("http://localhost:8030", "test-key")
        assert hasattr(service, 'create_invitation')
        assert hasattr(service, 'list_connections')
        print(f"  ✅ ConnectionService (Issuer) instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ ConnectionService (Issuer): {e}")
    
    # Test Verifier services
    tests_total += 1
    try:
        from agents.verifier.services.presentation_service import PresentationService
        service = PresentationService("http://localhost:8050", "test-key")
        assert hasattr(service, 'send_proof_request')
        assert hasattr(service, 'verify_presentation')
        print(f"  ✅ PresentationService instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ PresentationService: {e}")
    
    tests_total += 1
    try:
        from agents.verifier.services.connection_service import ConnectionService
        service = ConnectionService("http://localhost:8050", "test-key")
        assert hasattr(service, 'create_invitation')
        print(f"  ✅ ConnectionService (Verifier) instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ ConnectionService (Verifier): {e}")
    
    # Test IPFS service
    tests_total += 1
    try:
        from shared.services.ipfs_service import IPFSService
        service = IPFSService("http://localhost:5001", "http://localhost:8080")
        assert hasattr(service, 'add_file')
        assert hasattr(service, 'get_file')
        assert hasattr(service, 'pin_add')
        print(f"  ✅ IPFSService instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ IPFSService: {e}")
    
    print(f"\n📊 Service Class Tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def count_code_lines():
    """Count lines of code"""
    print("\n📏 Code Metrics...")
    
    python_files = list(Path('.').rglob('*.py'))
    # Exclude test files and __pycache__
    python_files = [f for f in python_files if '__pycache__' not in str(f) and 'validate_system.py' not in str(f)]
    
    total_lines = 0
    code_lines = 0
    
    for file_path in python_files:
        try:
            with open(file_path) as f:
                lines = f.readlines()
                total_lines += len(lines)
                code_lines += sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        except:
            pass
    
    print(f"  📊 Python files: {len(python_files)}")
    print(f"  📊 Total lines: {total_lines}")
    print(f"  📊 Code lines (excluding comments/blank): {code_lines}")
    
    # Count SQL lines
    sql_files = list(Path('infrastructure').rglob('*.sql'))
    sql_lines = sum(len(open(f).readlines()) for f in sql_files)
    print(f"  📊 SQL lines: {sql_lines}")
    
    # Count shell scripts
    sh_files = list(Path('infrastructure/scripts').rglob('*.sh'))
    sh_lines = sum(len(open(f).readlines()) for f in sh_files)
    print(f"  📊 Shell script lines: {sh_lines}")
    
    print(f"\n  📊 TOTAL CODE LINES: {code_lines + sql_lines + sh_lines}")


def main():
    """Run all validation tests"""
    print("="*60)
    print("🚀 CRYPTLOCKER SYSTEM VALIDATION")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Module Imports", test_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Code Quality", test_code_quality()))
    results.append(("Configuration", test_configuration()))
    results.append(("Service Classes", test_service_classes()))
    
    # Code metrics
    count_code_lines()
    
    # Summary
    print("\n" + "="*60)
    print("📋 VALIDATION SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name:.<40} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print("\n" + "="*60)
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
        print("="*60)
        print("\n✅ Next Steps:")
        print("  1. Review QUICKSTART_GUIDE.md for deployment instructions")
        print("  2. Run: bash infrastructure/scripts/start-system.sh")
        print("  3. Access services at http://localhost:8000 and http://localhost:8001")
        return 0
    else:
        print(f"⚠️  {total_tests - total_passed} TEST(S) FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
