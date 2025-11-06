#!/usr/bin/env python3
"""
Generate Synthetic Datasets for AIBPB Evaluation
"""

import numpy as np
import pandas as pd
import yaml
from pathlib import Path
from faker import Faker
import json
from tqdm import tqdm

class DatasetGenerator:
    def __init__(self, config_path='experiments/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.seed = self.config['simulation']['random_seed']
        np.random.seed(self.seed)
        self.fake = Faker()
        Faker.seed(self.seed)
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def generate_healthcare_dataset(self):
        """Generate synthetic healthcare cohort data"""
        print("Generating healthcare dataset...")
        
        config = self.config['datasets']['healthcare']
        n = config['num_patients']
        
        data = {
            'patient_id': [f'P{i:06d}' for i in range(n)],
            'age': np.random.randint(config['age_range'][0], 
                                     config['age_range'][1], n),
            'gender': np.random.choice(['M', 'F'], n),
            'diagnosis_code': [f'ICD{np.random.randint(1, config["diagnosis_codes"]):03d}' 
                             for _ in range(n)],
            'treatment_duration': np.random.exponential(30, n).astype(int),
            'outcome_score': np.random.normal(70, 15, n).clip(0, 100)
        }
        
        df = pd.DataFrame(data)
        df.to_csv(self.data_dir / 'healthcare.csv', index=False)
        
        print(f"  Generated {n} patient records")
        return df
    
    def generate_financial_dataset(self):
        """Generate synthetic financial transaction data"""
        print("Generating financial transaction dataset...")
        
        config = self.config['datasets']['financial']
        n = config['num_transactions']
        
        # Power-law distribution for amounts
        amounts = np.random.pareto(1.5, n) * 1000
        amounts = amounts.clip(config['amount_range'][0], 
                              config['amount_range'][1])
        
        data = {
            'transaction_id': [f'TX{i:08d}' for i in range(n)],
            'timestamp': pd.date_range('2023-01-01', periods=n, freq='5min'),
            'sender_id': [f'ACC{np.random.randint(1, 10000):05d}' for _ in range(n)],
            'receiver_id': [f'ACC{np.random.randint(1, 10000):05d}' for _ in range(n)],
            'amount': amounts,
            'risk_score': np.random.uniform(0, 1, n),
            'risk_category': np.random.randint(0, config['risk_categories'], n)
        }
        
        df = pd.DataFrame(data)
        df.to_csv(self.data_dir / 'financial.csv', index=False)
        
        print(f"  Generated {n} transaction records")
        return df
    
    def generate_federated_learning_dataset(self):
        """Generate synthetic federated learning model updates"""
        print("Generating federated learning dataset...")
        
        config = self.config['datasets']['federated_learning']
        n_clients = config['num_clients']
        
        # Simulate model gradients for MNIST (simplified)
        gradient_dim = 100  # Simplified gradient dimension
        
        data = []
        for client_id in tqdm(range(n_clients), desc="  Generating client data"):
            client_data = {
                'client_id': f'CLIENT{client_id:03d}',
                'gradients': np.random.randn(gradient_dim).tolist(),
                'loss': np.random.exponential(0.5),
                'accuracy': np.random.beta(8, 2),  # Biased towards high accuracy
                'data_size': np.random.randint(100, 1000)
            }
            data.append(client_data)
        
        with open(self.data_dir / 'federated_learning.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  Generated data for {n_clients} clients")
        return data
    
    def generate_all_datasets(self):
        """Generate all synthetic datasets"""
        print("\n" + "="*80)
        print("SYNTHETIC DATASET GENERATION".center(80))
        print("="*80 + "\n")
        
        datasets = {}
        
        # Generate each dataset type
        datasets['healthcare'] = self.generate_healthcare_dataset()
        datasets['financial'] = self.generate_financial_dataset()
        datasets['federated_learning'] = self.generate_federated_learning_dataset()
        
        # Generate metadata
        metadata = {
            'generated_at': pd.Timestamp.now().isoformat(),
            'random_seed': self.seed,
            'datasets': {
                'healthcare': {
                    'records': len(datasets['healthcare']),
                    'file': 'healthcare.csv'
                },
                'financial': {
                    'records': len(datasets['financial']),
                    'file': 'financial.csv'
                },
                'federated_learning': {
                    'clients': len(datasets['federated_learning']),
                    'file': 'federated_learning.json'
                }
            }
        }
        
        with open(self.data_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✓ All datasets generated successfully")
        print(f"  Location: {self.data_dir}")
        print(f"  Metadata: {self.data_dir / 'metadata.json'}")

def main():
    generator = DatasetGenerator()
    generator.generate_all_datasets()

if __name__ == '__main__':
    main()
