#!/bin/bash
# Quick Start Script for AIBPB Simulation
# This script sets up the environment and runs a quick test

set -e  # Exit on error

echo "=========================================="
echo "AIBPB Simulation Quick Start"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python3 --version || { echo -e "${RED}Python 3 not found. Please install Python 3.8+${NC}"; exit 1; }

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

# Check Node.js
echo -e "${YELLOW}Checking Node.js...${NC}"
node --version || { echo -e "${RED}Node.js not found. Please install Node.js 14+${NC}"; exit 1; }

# Install Node.js dependencies
echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "=========================================="
echo "Running Quick Test"
echo "=========================================="
echo ""

# Set environment variable for quick test
export QUICK_TEST=1
export RANDOM_SEED=42

# Run quick test with small datasets
echo -e "${YELLOW}Step 1/4: Generating test datasets...${NC}"
python3 experiments/generate_datasets.py

echo -e "${YELLOW}Step 2/4: Running performance test...${NC}"
python3 experiments/performance_evaluation.py

echo -e "${YELLOW}Step 3/4: Running privacy analysis...${NC}"
python3 experiments/privacy_analysis.py

echo -e "${YELLOW}Step 4/4: Generating sample figures...${NC}"
python3 experiments/generate_figures.py

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Quick test completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. View generated figures: ls -lh figures/"
echo "  2. View results: ls -lh results/"
echo "  3. Run full experiments: python run_all_experiments.py"
echo ""
echo "For more information, see README.md"
echo ""
