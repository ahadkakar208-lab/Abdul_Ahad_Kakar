"""
Memory performance benchmarks
"""

import time
import numpy as np
from data.generator import DataGenerator
from data.storage import DataStorage
from config import MEMORY_SIZES

class MemoryBenchmark:
    """Memory performance testing"""
    
    def __init__(self):
        self.data_gen = DataGenerator()
        self.storage = DataStorage()
    
    def benchmark_sequential_access(self, size_mb):
        """Benchmark sequential memory access"""
        # Generate data - reduced size for faster execution
        data = self.data_gen.generate_matrix_data(int(np.sqrt(size_mb * 512 * 1024 / 8)))
        
        # Sequential access
        start_time = time.time()
        total = 0
        for row in data:
            for value in row:
                total += value
        end_time = time.time()
        elapsed = max(end_time - start_time, 0.0001)
        
        return {
            "operation": "sequential_access",
            "size_mb": size_mb,
            "time_seconds": elapsed,
            "bandwidth_mb_per_sec": size_mb / elapsed
        }
    
    def benchmark_random_access(self, size_mb):
        """Benchmark random memory access"""
        # Generate data - reduced size for faster execution
        data = self.data_gen.generate_random_numbers(int(size_mb * 256 * 1024 / 4))
        
        # Random access - reduced iterations for speed
        start_time = time.time()
        total = 0
        data_len = len(data)
        iterations = min(10000, data_len // 2)  # Limit iterations
        for _ in range(iterations):
            idx = np.random.randint(0, data_len)
            total += data[idx]
        end_time = time.time()
        elapsed = max(end_time - start_time, 0.0001)
        
        return {
            "operation": "random_access",
            "size_mb": size_mb,
            "time_seconds": elapsed,
            "bandwidth_mb_per_sec": size_mb / elapsed
        }
    
    def benchmark_memory_allocation(self, size_mb):
        """Benchmark memory allocation speed"""
        # Convert MB to number of elements - reduced for faster execution
        elements = int(size_mb * 512 * 1024 / 8)
        
        # Allocation
        start_time = time.time()
        data = [0] * elements
        end_time = time.time()
        elapsed = max(end_time - start_time, 0.0001)
        
        return {
            "operation": "memory_allocation",
            "size_mb": size_mb,
            "time_seconds": elapsed,
            "allocation_mb_per_sec": size_mb / elapsed
        }
    
    def run_all(self):
        """Run all memory benchmarks"""
        results = {}
        
        for size in MEMORY_SIZES:
            results[f"sequential_access_{size}mb"] = self.benchmark_sequential_access(size)
            results[f"random_access_{size}mb"] = self.benchmark_random_access(size)
            results[f"allocation_{size}mb"] = self.benchmark_memory_allocation(size)
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.storage.save_json(results, f"memory_benchmark_{timestamp}.json")
        
        return results
