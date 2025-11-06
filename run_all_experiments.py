#!/usr/bin/env python3
"""
AIBPB Complete Experiment Runner
Executes all experiments and generates results for the research paper
"""

import sys
import os
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import yaml
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ExperimentRunner:
    def __init__(self, config_path='experiments/config.yaml'):
        self.config = self.load_config(config_path)
        self.start_time = None
        self.results_dir = Path(self.config['output']['results_dir'])
        self.figures_dir = Path(self.config['output']['figures_dir'])
        
        # Create directories
        self.results_dir.mkdir(exist_ok=True)
        self.figures_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_path):
        """Load experiment configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}{text.center(80)}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    def print_step(self, step_num, total_steps, description):
        """Print step information"""
        print(f"{Fore.GREEN}[Step {step_num}/{total_steps}]{Style.RESET_ALL} {description}")
    
    def run_command(self, cmd, description):
        """Run a command and track time"""
        print(f"{Fore.YELLOW}Running: {description}...{Style.RESET_ALL}")
        start = time.time()
        
        try:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  capture_output=True, text=True)
            elapsed = time.time() - start
            print(f"{Fore.GREEN}✓ Completed in {elapsed:.1f}s{Style.RESET_ALL}")
            return True
        except subprocess.CalledProcessError as e:
            elapsed = time.time() - start
            print(f"{Fore.RED}✗ Failed after {elapsed:.1f}s{Style.RESET_ALL}")
            print(f"{Fore.RED}Error: {e.stderr}{Style.RESET_ALL}")
            return False
    
    def run_dataset_generation(self):
        """Generate synthetic datasets"""
        self.print_step(1, 6, "Generating Synthetic Datasets")
        return self.run_command(
            "python experiments/generate_datasets.py",
            "Dataset generation"
        )
    
    def run_circuit_compilation(self):
        """Compile ZKP circuits"""
        self.print_step(2, 6, "Compiling Zero-Knowledge Proof Circuits")
        return self.run_command(
            "node scripts/compile_circuits.js",
            "Circuit compilation"
        )
    
    def run_performance_evaluation(self):
        """Run performance experiments"""
        self.print_step(3, 6, "Running Performance Evaluation")
        return self.run_command(
            "python experiments/performance_evaluation.py",
            "Performance experiments"
        )
    
    def run_privacy_analysis(self):
        """Run privacy analysis"""
        self.print_step(4, 6, "Running Privacy Analysis")
        return self.run_command(
            "python experiments/privacy_analysis.py",
            "Privacy analysis"
        )
    
    def run_compliance_evaluation(self):
        """Run compliance evaluation"""
        self.print_step(5, 6, "Running Compliance Evaluation")
        return self.run_command(
            "python experiments/compliance_evaluation.py",
            "Compliance evaluation"
        )
    
    def run_figure_generation(self):
        """Generate all figures"""
        self.print_step(6, 6, "Generating Figures for Paper")
        return self.run_command(
            "python experiments/generate_figures.py",
            "Figure generation"
        )
    
    def print_summary(self, success_steps, total_steps):
        """Print execution summary"""
        self.print_header("EXECUTION SUMMARY")
        
        elapsed = time.time() - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        print(f"Total execution time: {hours}h {minutes}m {seconds}s")
        print(f"Successful steps: {success_steps}/{total_steps}")
        
        if success_steps == total_steps:
            print(f"\n{Fore.GREEN}✓ All experiments completed successfully!{Style.RESET_ALL}")
            print(f"\nResults saved to: {self.results_dir}")
            print(f"Figures saved to: {self.figures_dir}")
            print(f"\nGenerated figures:")
            for fig in sorted(self.figures_dir.glob('*.pdf')):
                print(f"  - {fig.name}")
        else:
            print(f"\n{Fore.RED}✗ Some experiments failed. Check logs for details.{Style.RESET_ALL}")
    
    def run_all(self):
        """Run all experiments"""
        self.print_header("AIBPB SIMULATION FRAMEWORK")
        print(f"Starting experiments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = time.time()
        
        steps = [
            self.run_dataset_generation,
            self.run_circuit_compilation,
            self.run_performance_evaluation,
            self.run_privacy_analysis,
            self.run_compliance_evaluation,
            self.run_figure_generation
        ]
        
        success_count = 0
        for step in steps:
            if step():
                success_count += 1
            else:
                print(f"{Fore.YELLOW}Warning: Step failed but continuing...{Style.RESET_ALL}")
        
        self.print_summary(success_count, len(steps))
        
        return success_count == len(steps)

def main():
    parser = argparse.ArgumentParser(
        description='Run AIBPB simulation experiments'
    )
    parser.add_argument(
        '--config',
        default='experiments/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--quick-test',
        action='store_true',
        help='Run quick test with small datasets'
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['RANDOM_SEED'] = str(args.seed)
    if args.quick_test:
        os.environ['QUICK_TEST'] = '1'
    
    # Run experiments
    runner = ExperimentRunner(args.config)
    success = runner.run_all()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
