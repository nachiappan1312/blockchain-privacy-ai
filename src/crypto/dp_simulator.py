"""
Differential Privacy Simulator
Simulates DP noise addition and privacy budget management
"""

import numpy as np
import time

class DPSimulator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.privacy_budget = {}
    
    def add_noise(self, dataset_size, epsilon=1.0):
        """
        Simulate differential privacy noise addition
        Very fast operation
        """
        # DP noise addition is very fast
        noise_time = 0.00001 * dataset_size  # Extremely fast
        time.sleep(max(noise_time, 0.0001))
        
        return noise_time
    
    def laplace_mechanism(self, true_value, sensitivity, epsilon):
        """Add Laplace noise for differential privacy"""
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale)
        return true_value + noise
    
    def gaussian_mechanism(self, true_value, sensitivity, epsilon, delta=1e-5):
        """Add Gaussian noise for differential privacy"""
        sigma = np.sqrt(2 * np.log(1.25/delta)) * sensitivity / epsilon
        noise = np.random.normal(0, sigma)
        return true_value + noise
    
    def calculate_composition(self, epsilons):
        """Calculate composed privacy budget"""
        # Basic composition
        return sum(epsilons)
    
    def estimate_privacy_loss(self, epsilon, num_queries):
        """Estimate privacy loss over multiple queries"""
        return epsilon * np.sqrt(num_queries)  # Advanced composition
