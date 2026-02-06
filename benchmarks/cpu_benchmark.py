"""
CPU performance benchmarks
"""

import time
import numpy as np
from data.generator import DataGenerator
from data.storage import DataStorage

class CPUBenchmark:
    """CPU performance testing"""
    
    def __init__(self):
        self.data_gen = DataGenerator()
        self.storage = DataStorage()
    
    def benchmark_integer_operations(self, iterations=1000000):
        """Benchmark integer arithmetic operations"""
        start_time = time.time()
        
        result = 0
        for i in range(iterations):
            result += i * 2
            result -= i // 3
            result *= 2
            result //= 4
        
        end_time = time.time()
        elapsed = max(end_time - start_time, 0.0001)  # Avoid division by zero
        return {
            "operation": "integer_arithmetic",
            "iterations": iterations,
            "time_seconds": elapsed,
            "operations_per_second": iterations / elapsed
        }
    
    def benchmark_floating_point_operations(self, size=1000):
        """Benchmark floating point operations using matrix multiplication"""
        matrix_a = self.data_gen.generate_matrix_data(size)
        matrix_b = self.data_gen.generate_matrix_data(size)
        
        start_time = time.time()
        result = np.dot(matrix_a, matrix_b)
        end_time = time.time()
        
        # Calculate operations (2*n^3 for matrix multiplication)
        operations = 2 * (size ** 3)
        elapsed = max(end_time - start_time, 0.0001)  # Avoid division by zero
        
        return {
            "operation": "matrix_multiplication",
            "matrix_size": size,
            "time_seconds": elapsed,
            "flops": operations / elapsed
        }
    
    def benchmark_prime_calculation(self, limit=10000):
        """Benchmark prime number calculation"""
        def is_prime(n):
            if n <= 1:
                return False
            if n <= 3:
                return True
            if n % 2 == 0 or n % 3 == 0:
                return False
            i = 5
            w = 2
            while i * i <= n:
                if n % i == 0:
                    return False
                i += w
                w = 6 - w
            return True
        
        start_time = time.time()
        primes = [i for i in range(2, limit) if is_prime(i)]
        end_time = time.time()
        elapsed = max(end_time - start_time, 0.0001)  # Avoid division by zero
        
        return {
            "operation": "prime_calculation",
            "limit": limit,
            "primes_found": len(primes),
            "time_seconds": elapsed,
            "numbers_per_second": limit / elapsed
        }
    
    def run_all(self):
        """Run all CPU benchmarks"""
        results = {
            "integer_ops": self.benchmark_integer_operations(500000),
            "floating_point_ops_small": self.benchmark_floating_point_operations(50),
            "floating_point_ops_medium": self.benchmark_floating_point_operations(150),
            "prime_calculation": self.benchmark_prime_calculation(5000)
        }
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.storage.save_json(results, f"cpu_benchmark_{timestamp}.json")
        
        return results
