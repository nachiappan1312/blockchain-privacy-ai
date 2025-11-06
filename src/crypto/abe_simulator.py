"""
Attribute-Based Encryption Simulator
Simulates ABE encryption and decryption operations
"""

import numpy as np
import time

class ABESimulator:
    def __init__(self, seed=42):
        np.random.seed(seed)
    
    def encrypt(self, dataset_size, num_attributes):
        """
        Simulate ABE encryption
        Time scales with number of attributes and data size
        """
        # Encryption time increases with attributes
        base_time = 0.0002 * num_attributes
        size_factor = np.log(dataset_size) / 10
        
        encrypt_time = base_time * size_factor * (1 + np.random.normal(0, 0.1))
        time.sleep(max(encrypt_time, 0.001))
        
        # Generate mock ciphertext
        ciphertext = {
            'policy': self._generate_policy(num_attributes),
            'encrypted_data': np.random.bytes(dataset_size // 100),
            'num_attributes': num_attributes
        }
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Simulate ABE decryption"""
        num_attributes = ciphertext['num_attributes']
        
        # Decryption time scales with attributes
        decrypt_time = 0.0003 * num_attributes * (1 + np.random.normal(0, 0.1))
        time.sleep(max(decrypt_time, 0.001))
        
        # Return mock plaintext
        return b"decrypted_data"
    
    def _generate_policy(self, num_attributes):
        """Generate mock access policy"""
        attributes = [f"attr_{i}" for i in range(num_attributes)]
        return " AND ".join(attributes)
