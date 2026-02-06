"""
Parallel processing benchmarks
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from data.generator import DataGenerator
from data.storage import DataStorage
from config import PARALLEL_TASK_SIZES, PARALLEL_THREAD_COUNTS

class ParallelBenchmark:
    """Parallel processing performance testing"""
    
    def __init__(self):
        self.data_gen = DataGenerator()
        self.storage = DataStorage()
    
    def cpu_intensive_task(self, n):
        """CPU intensive task for parallel testing"""
        # Prime number calculation
        def is_prime(num):
            if num <= 1:
                return False
            if num <= 3:
                return True
            if num % 2 == 0 or num % 3 == 0:
                return False
            i = 5
            w = 2
            while i * i <= num:
                if num % i == 0:
                    return False
                i += w
                w = 6 - w
            return True
        
        primes = []
        for i in range(n):
            if is_prime(i):
                primes.append(i)
        return len(primes)
    
    def benchmark_threading(self, task_size, thread_count):
        """Benchmark threading performance"""
        chunk_size = task_size // thread_count
        chunks = [chunk_size] * thread_count
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            results = list(executor.map(self.cpu_intensive_task, chunks))
        total_primes = sum(results)
        end_time = time.time()
        
        elapsed = max(end_time - start_time, 0.0001)
        return {
            "method": "threading",
            "task_size": task_size,
            "thread_count": thread_count,
            "time_seconds": elapsed,
            "tasks_per_second": task_size / elapsed,
            "total_primes": total_primes
        }
    
    def benchmark_multiprocessing(self, task_size, process_count):
        """Benchmark multiprocessing performance"""
        chunk_size = task_size // process_count
        chunks = [chunk_size] * process_count
        
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=process_count) as executor:
            results = list(executor.map(self.cpu_intensive_task, chunks))
        total_primes = sum(results)
        end_time = time.time()
        
        elapsed = max(end_time - start_time, 0.0001)
        return {
            "method": "multiprocessing",
            "task_size": task_size,
            "process_count": process_count,
            "time_seconds": elapsed,
            "tasks_per_second": task_size / elapsed,
            "total_primes": total_primes
        }
    
    def benchmark_sequential(self, task_size):
        """Benchmark sequential execution for comparison"""
        start_time = time.time()
        primes = self.cpu_intensive_task(task_size)
        end_time = time.time()
        
        elapsed = max(end_time - start_time, 0.0001)
        return {
            "method": "sequential",
            "task_size": task_size,
            "time_seconds": elapsed,
            "tasks_per_second": task_size / elapsed,
            "total_primes": primes
        }
    
    def run_all(self):
        """Run all parallel benchmarks"""
        results = {}
        
        # Sequential benchmarks for comparison
        for size in PARALLEL_TASK_SIZES:
            results[f"sequential_{size}"] = self.benchmark_sequential(size)
        
        # Threading benchmarks
        for size in PARALLEL_TASK_SIZES:
            for threads in PARALLEL_THREAD_COUNTS:
                results[f"threading_{size}_{threads}"] = self.benchmark_threading(size, threads)
        
        # Multiprocessing benchmarks
        for size in PARALLEL_TASK_SIZES:
            for processes in PARALLEL_THREAD_COUNTS:
                results[f"multiprocessing_{size}_{processes}"] = self.benchmark_multiprocessing(size, processes)
        
        # Save results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.storage.save_json(results, f"parallel_benchmark_{timestamp}.json")
        
        return results
