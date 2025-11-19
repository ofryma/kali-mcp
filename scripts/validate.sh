#!/bin/bash

# Validation script for Kali MCP Server repository
# This script performs various checks to ensure repository integrity

set -e  # Exit on any error

echo "🔍 Starting repository validation..."
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for errors
ERRORS=0

# Function to print error
print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

echo "📋 Checking required files..."
# Check for required files
REQUIRED_FILES=(
    "README.md"
    "requirements.txt"
    "LICENSE"
    "Dockerfile"
    "docker-compose.yml"
    "kali_server.py"
    "mcp_http_server.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found $file"
    else
        print_error "Missing required file: $file"
    fi
done

echo ""
echo "🐍 Validating Python syntax..."
# Check Python syntax for all .py files
PYTHON_FILES=$(find . -name "*.py" -not -path "./.git/*" -not -path "./__pycache__/*" -not -path "*/__pycache__/*")

for file in $PYTHON_FILES; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        print_success "Valid syntax: $file"
    else
        print_error "Syntax error in: $file"
    fi
done

echo ""
echo "📦 Checking tool directory structure..."
# Check that all tool directories have __init__.py
TOOL_DIRS=$(find server/tools -type d -not -path "*/__pycache__")

for dir in $TOOL_DIRS; do
    if [ -f "$dir/__init__.py" ]; then
        print_success "Found __init__.py in $dir"
    else
        print_warning "Missing __init__.py in $dir"
    fi
done

echo ""
echo "📝 Validating requirements.txt..."
# Check if requirements.txt has valid format
if grep -E "^[a-zA-Z0-9_-]+([><=!~]=.*)?$|^#.*$|^$" requirements.txt > /dev/null; then
    print_success "requirements.txt format looks valid"
else
    print_error "requirements.txt contains invalid entries"
fi

echo ""
echo "🔍 Checking for common issues..."
# Check for .pyc files in git (shouldn't be there)
if find . -name "*.pyc" -not -path "./.git/*" | grep -q "."; then
    print_warning "Found .pyc files in repository (should be in .gitignore)"
fi

# Check for __pycache__ directories
if find . -name "__pycache__" -not -path "./.git/*" | grep -q "."; then
    print_warning "Found __pycache__ directories (should be in .gitignore)"
fi

# Check for common sensitive patterns (basic check)
if grep -r "password.*=.*['\"]" --include="*.py" . 2>/dev/null | grep -v "# " | grep -v "args.password" | grep -v "password_file" | grep -q .; then
    print_warning "Potential hardcoded password found (please review)"
fi

echo ""
echo "🎯 Checking Python imports..."
# Check for common import issues
if grep -r "from \* import" --include="*.py" . 2>/dev/null | grep -q .; then
    print_warning "Found 'from * import' statements (not recommended)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Final summary
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✨ Validation completed successfully! No errors found.${NC}"
    exit 0
else
    echo -e "${RED}❌ Validation failed with $ERRORS error(s).${NC}"
    exit 1
fi

