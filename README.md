# AIBPB Simulation Framework

AI-Brokered Privacy on Blockchain - Complete Simulation and Evaluation Framework

## Overview

This repository contains a complete simulation framework for evaluating the AIBPB (AI-Brokered Privacy on Blockchain) system. It includes:
- Zero-knowledge proof generation using Circom/snarkjs
- Attribute-based encryption simulation
- Differential privacy mechanisms
- Smart contract deployment and verification
- AI broker optimization algorithms
- Comprehensive evaluation metrics and visualization

## System Requirements

- macOS 11 (Big Sur) or later
- Python 3.11 (recommended for package compatibility)
- Node.js 14+
- 8GB RAM minimum (16GB recommended)
- 10GB free disk space

## Installation

### Step 1: Install System Dependencies

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js and npm
brew install node@16
# Add Node 16 to PATH
echo 'export PATH="/usr/local/opt/node@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install Python (macOS includes Python 3, but you can install a specific version)
brew install python@3.11

# Install build tools and dependencies
# Install Xcode Command Line Tools (required for compilation)
xcode-select --install

# Install required libraries
brew install gmp openssl
```

### Step 2: Clone and Setup Repository

```bash
# Navigate to the project directory
cd aibpb-simulation

# Create Python virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Step 3: Install Circom and snarkjs

```bash
# Install Rust (required for Circom compilation)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Circom compiler
cd ~
git clone https://github.com/iden3/circom.git
cd circom
cargo build --release
cargo install --path circom

# Ensure Cargo binaries are in PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install snarkjs globally
npm install -g snarkjs

# Return to project directory
cd ~/aibpb-simulation
```

## Project Structure

```
aibpb-simulation/
├── src/                        # Source code
│   ├── ai_broker/             # AI broker implementation
│   ├── crypto/                # Cryptographic primitives
│   ├── blockchain/            # Blockchain simulation
│   └── utils/                 # Utility functions
├── circuits/                   # Circom ZKP circuits
├── contracts/                  # Solidity smart contracts
├── data/                      # Synthetic datasets
├── experiments/               # Experiment configurations
├── results/                   # Experimental results
├── figures/                   # Generated plots and figures
└── docs/                      # Documentation

```

## Quick Start

### Generate All Results (Complete Simulation)

```bash
# Activate virtual environment
source venv/bin/activate

# Run complete experimental pipeline
python run_all_experiments.py

# This will:
# 1. Generate synthetic datasets (10-15 minutes)
# 2. Compile ZKP circuits (5-10 minutes)
# 3. Run performance experiments (20-30 minutes)
# 4. Run privacy analysis (15-20 minutes)
# 5. Run compliance tests (10-15 minutes)
# 6. Generate all figures (5 minutes)
# Total time: ~1.5-2 hours
```

### Run Individual Experiments

```bash
# 1. Generate synthetic datasets
python experiments/generate_datasets.py

# 2. Performance evaluation
python experiments/performance_evaluation.py

# 3. Privacy analysis
python experiments/privacy_analysis.py

# 4. Compliance testing
python experiments/compliance_evaluation.py

# 5. Cost-privacy trade-off analysis
python experiments/tradeoff_analysis.py

# 6. Generate all figures
python experiments/generate_figures.py
```

## Experiment Details

### 1. Performance Evaluation
- **Script**: `experiments/performance_evaluation.py`
- **Duration**: 20-30 minutes
- **Outputs**: 
  - `results/performance_metrics.json`
  - `figures/proof_generation_time.pdf`
  - `figures/gas_consumption.pdf`

### 2. Privacy Analysis
- **Script**: `experiments/privacy_analysis.py`
- **Duration**: 15-20 minutes
- **Outputs**:
  - `results/privacy_metrics.json`
  - `figures/information_leakage.pdf`
  - `figures/k_anonymity.pdf`

### 3. Compliance Evaluation
- **Script**: `experiments/compliance_evaluation.py`
- **Duration**: 10-15 minutes
- **Outputs**:
  - `results/compliance_scores.json`
  - `figures/policy_satisfaction.pdf`

### 4. Trade-off Analysis
- **Script**: `experiments/tradeoff_analysis.py`
- **Duration**: 25-35 minutes
- **Outputs**:
  - `results/pareto_frontier.json`
  - `figures/cost_privacy_tradeoff.pdf`

## Generated Figures for Paper

All figures are saved in PDF format (high quality for LaTeX):

1. **Figure 1**: System Architecture Diagram
2. **Figure 2**: Proof Generation Time vs Dataset Size
3. **Figure 3**: Gas Consumption Comparison
4. **Figure 4**: Information Leakage Analysis
5. **Figure 5**: K-Anonymity Measurements
6. **Figure 6**: Policy Satisfaction Rates
7. **Figure 7**: Cost-Privacy Pareto Frontier
8. **Figure 8**: Scalability Analysis
9. **Figure 9**: Baseline Comparison

## Interpreting Results

### Performance Metrics
- **Proof Generation Time**: Lower is better (target: <10s for 10K records)
- **Gas Consumption**: Lower is better (target: <500K gas)
- **Throughput**: Higher is better (target: >200 proofs/hour)

### Privacy Metrics
- **Information Leakage**: Lower is better (target: <0.1 bits)
- **K-Anonymity**: Higher is better (target: k≥500 for HIPAA)
- **Differential Privacy ε**: Lower is better (target: ε≤1.0)

### Compliance Metrics
- **Policy Satisfaction**: Higher is better (target: >95%)
- **Completeness Score**: Higher is better (target: >90%)

## Customization

### Modify Experiment Parameters

Edit `experiments/config.yaml`:

```yaml
datasets:
  sizes: [1000, 5000, 10000, 50000, 100000]
  
privacy:
  epsilon_values: [0.1, 0.5, 1.0, 2.0, 4.0]
  
optimization:
  alpha_values: [0.0, 0.25, 0.5, 0.75, 1.0]
  
simulation:
  num_trials: 50
  random_seed: 42
```

### Add Custom Datasets

Place CSV files in `data/custom/` and update `experiments/dataset_config.py`

## Troubleshooting

### Issue: pip install fails with "Cannot import 'setuptools.build_meta'" error
This occurs when using Python 3.13, which is too new for the packages in requirements.txt.

**Solution:**
```bash
# Install Python 3.11
brew install python@3.11

# Remove existing venv and recreate with Python 3.11
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
```

**Why?** Python 3.13 (released Oct 2024) is too new. Many scientific packages in requirements.txt (from 2023) don't have pre-built wheels for Python 3.13 yet, and building from source fails due to missing build dependencies.

### Issue: Circom compilation fails
```bash
# Reinstall Circom with correct Rust version
rustup install stable
rustup default stable
cargo install --path circom --force
```

### Issue: Out of memory during large experiments
```bash
# Reduce dataset sizes in config.yaml
# Or close other applications to free up memory
# macOS manages swap automatically, but you can monitor memory:
vm_stat
# Consider increasing available RAM or reducing experiment sizes
```

### Issue: snarkjs not found
```bash
# Install snarkjs locally
npm install snarkjs
# Update PATH in experiments
export NODE_PATH=$(npm root -g)
```

## Reproducibility

All experiments use fixed random seeds for reproducibility:
- Dataset generation: seed=42
- Circuit compilation: deterministic
- Blockchain simulation: fixed genesis block

To reproduce exact results:
```bash
python run_all_experiments.py --seed 42 --deterministic
```

## Performance Optimization

### For faster execution:
```bash
# Run with parallelization (uses all CPU cores)
python run_all_experiments.py --parallel

# Skip slow experiments
python run_all_experiments.py --skip-large-scale

# Use smaller datasets for testing
python run_all_experiments.py --quick-test
```

## Citation

If you use this simulation framework in your research, please cite:

```bibtex
@inproceedings{aibpb2025,
  title={Blockchain-Based Privacy Solutions Brokered with AI for Data Integrity and Compliance},
  author={Author, First and Author, Second},
  booktitle={IEEE TRON Conference},
  year={2025}
}
```

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [repository]/issues
- Email: author@example.com

## macOS-Specific Notes

### Python Version Requirements
- **Use Python 3.11** for best compatibility with all packages
- Python 3.13 is **not compatible** - many packages don't have wheels for it yet
- Install Python 3.11 via Homebrew: `brew install python@3.11`
- Always use `python3.11 -m venv venv` when creating virtual environments

### Shell Configuration
- The instructions above use `~/.zshrc` (default shell in macOS 10.15+)
- If using bash, replace `~/.zshrc` with `~/.bash_profile` or `~/.bashrc`

### Homebrew Installation Paths
- Apple Silicon (M1/M2/M3): Homebrew installs to `/opt/homebrew`
- Intel Macs: Homebrew installs to `/usr/local`
- Adjust PATH commands if needed based on your Mac architecture

### Performance Notes
- Apple Silicon Macs may see significantly faster performance in crypto operations
- Ensure Rosetta 2 is installed if running on Apple Silicon: `softwareupdate --install-rosetta`

### Common Issues
- If `xcode-select --install` fails, install from Mac App Store or run: `sudo xcode-select --reset`
- For M1/M2/M3 Macs, some npm packages may need Rosetta 2 compatibility
- If Node.js path issues persist, use: `brew link node@16 --force --overwrite`

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.
