"""
Blockchain Gas Estimator
Estimates gas consumption for various operations
"""

import numpy as np

class GasEstimator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        
        # Base gas costs (approximate for Ethereum)
        self.base_costs = {
            'transaction': 21000,
            'storage_word': 20000,
            'pairing': 100000,
            'hash': 30
        }
    
    def estimate_zkp_verification(self, circuit_size):
        """
        Estimate gas for ZKP verification
        Groth16: ~250K-300K gas regardless of circuit size
        """
        base_gas = 250000
        variance = np.random.randint(-10000, 10000)
        return base_gas + variance
    
    def estimate_abe_verification(self, num_attributes):
        """Estimate gas for ABE policy verification"""
        # Gas increases with policy complexity
        base_gas = 50000
        attribute_cost = 10000 * num_attributes
        return base_gas + attribute_cost
    
    def estimate_merkle_verification(self, tree_depth):
        """Estimate gas for Merkle proof verification"""
        # Each hash operation costs ~30 gas
        hash_operations = tree_depth
        return self.base_costs['transaction'] + (hash_operations * self.base_costs['hash'])
    
    def estimate_naive_storage(self, dataset_size):
        """Estimate gas for naive on-chain storage"""
        # Very expensive - 20K gas per 32 bytes
        words_needed = dataset_size // 32
        return words_needed * self.base_costs['storage_word']
    
    def estimate_composite_proof(self, has_zkp=True, has_abe=True, 
                                 num_attributes=5, tree_depth=10):
        """Estimate gas for composite proof verification"""
        total_gas = self.base_costs['transaction']
        
        if has_zkp:
            total_gas += self.estimate_zkp_verification(16384)
        
        if has_abe:
            total_gas += self.estimate_abe_verification(num_attributes)
        
        # Merkle root verification
        total_gas += self.estimate_merkle_verification(tree_depth)
        
        return total_gas
