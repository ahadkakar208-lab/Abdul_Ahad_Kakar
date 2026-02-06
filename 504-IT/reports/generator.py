"""
Report generation for benchmark results
"""

import os
from datetime import datetime
from config import REPORTS_DIR, REPORT_TEMPLATE

class ReportGenerator:
    """Generate performance reports"""
    
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def format_cpu_results(self, cpu_results):
        """Format CPU benchmark results for report"""
        text = f"Integer Operations: {cpu_results['integer_ops']['operations_per_second']:.2f} ops/sec\n"
        text += f"Matrix Multiplication (Small): {cpu_results['floating_point_ops_small']['flops']:.2f} FLOPS\n"
        text += f"Matrix Multiplication (Medium): {cpu_results['floating_point_ops_medium']['flops']:.2f} FLOPS\n"
        text += f"Prime Calculation: {cpu_results['prime_calculation']['primes_found']} primes in {cpu_results['prime_calculation']['time_seconds']:.2f} seconds"
        return text
    
    def format_memory_results(self, mem_results):
        """Format memory benchmark results for report"""
        text = ""
        for key, result in mem_results.items():
            if "sequential_access" in key:
                text += f"Sequential Access ({result['size_mb']}MB): {result['bandwidth_mb_per_sec']:.2f} MB/sec\n"
            elif "random_access" in key:
                text += f"Random Access ({result['size_mb']}MB): {result['bandwidth_mb_per_sec']:.2f} MB/sec\n"
            elif "allocation" in key:
                text += f"Memory Allocation ({result['size_mb']}MB): {result['allocation_mb_per_sec']:.2f} MB/sec\n"
        return text
    
    def format_parallel_results(self, parallel_results):
        """Format parallel benchmark results for report"""
        text = ""
        
        # Find sequential results
        sequential_results = {k: v for k, v in parallel_results.items() if "sequential_" in k}
        for key, result in sequential_results.items():
            text += f"Sequential ({result['task_size']} tasks): {result['time_seconds']:.2f} seconds\n"
        
        # Find best threading result
        threading_results = {k: v for k, v in parallel_results.items() if "threading_" in k}
        if threading_results:
            best_threading = min(threading_results.values(), key=lambda x: x['time_seconds'])
            text += f"Best Threading ({best_threading['thread_count']} threads, {best_threading['task_size']} tasks): {best_threading['time_seconds']:.2f} seconds\n"
        
        # Find best multiprocessing result
        multiprocessing_results = {k: v for k, v in parallel_results.items() if "multiprocessing_" in k}
        if multiprocessing_results:
            best_multiprocessing = min(multiprocessing_results.values(), key=lambda x: x['time_seconds'])
            text += f"Best Multiprocessing ({best_multiprocessing['process_count']} processes, {best_multiprocessing['task_size']} tasks): {best_multiprocessing['time_seconds']:.2f} seconds\n"
        
        return text
    
    def generate_summary(self, results):
        """Generate a summary of the benchmark results"""
        system_info = results["system_info"]
        cpu_cores = system_info["cpu_cores"]
        total_memory = system_info["total_memory"]
        
        # Calculate speedup from parallel processing
        sequential_time = None
        best_parallel_time = None
        
        for key, result in results["parallel"].items():
            if "sequential_10000" in key:
                sequential_time = result["time_seconds"]
            elif "multiprocessing_10000_" in key:
                if best_parallel_time is None or result["time_seconds"] < best_parallel_time:
                    best_parallel_time = result["time_seconds"]
        
        speedup = "N/A"
        if sequential_time and best_parallel_time:
            speedup = f"{sequential_time / best_parallel_time:.2f}x"
        
        summary = f"System with {cpu_cores} CPU cores and {total_memory}GB of memory shows "
        summary += f"a parallel processing speedup of {speedup} with optimal configuration."
        
        return summary
    
    def create_report(self, results):
        """Create a comprehensive performance report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_info = results["system_info"]
        
        # Format results
        cpu_text = self.format_cpu_results(results["cpu"])
        memory_text = self.format_memory_results(results["memory"])
        parallel_text = self.format_parallel_results(results["parallel"])
        summary = self.generate_summary(results)
        
        # Generate report
        report_content = REPORT_TEMPLATE.format(
            timestamp=timestamp,
            os_name=system_info["os_name"],
            cpu_name=system_info["cpu_name"],
            cpu_cores=system_info["cpu_cores"],
            total_memory=system_info["total_memory"],
            cpu_results=cpu_text,
            memory_results=memory_text,
            parallel_results=parallel_text,
            summary=summary
        )
        
        # Save report
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"benchmark_report_{timestamp_str}.txt")
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return report_path
