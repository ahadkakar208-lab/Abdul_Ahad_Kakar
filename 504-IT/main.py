#!/usr/bin/env python3
"""
Hardware Performance Benchmarking Tool
Main entry point for the application
"""

import os
import sys
import time
import argparse
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.generator import DataGenerator
from benchmarks.cpu_benchmark import CPUBenchmark
from benchmarks.memory_benchmark import MemoryBenchmark
from benchmarks.parallel_benchmark import ParallelBenchmark
from visualization.charts import ChartGenerator
from reports.generator import ReportGenerator
from config import RESULTS_DIR, REPORTS_DIR

def ensure_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

def run_benchmarks():
    """Run all benchmarks and collect results"""
    print("Starting hardware benchmarking suite...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Initialize data generator
    data_gen = DataGenerator()
    
    # Generate test data
    print("Generating test data...")
    test_data = data_gen.generate_all()
    
    # Initialize benchmarks
    cpu_bench = CPUBenchmark()
    mem_bench = MemoryBenchmark()
    parallel_bench = ParallelBenchmark()
    
    # Run CPU benchmarks
    print("\nRunning CPU benchmarks...")
    cpu_results = cpu_bench.run_all()
    
    # Run memory benchmarks
    print("\nRunning memory benchmarks...")
    mem_results = mem_bench.run_all()
    
    # Run parallel benchmarks
    print("\nRunning parallel processing benchmarks...")
    parallel_results = parallel_bench.run_all()
    
    # Combine all results
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "system_info": data_gen.get_system_info(),
        "cpu": cpu_results,
        "memory": mem_results,
        "parallel": parallel_results
    }
    
    return all_results

def visualize_results(results):
    """Generate visualization charts"""
    print("\nGenerating visualization charts...")
    chart_gen = ChartGenerator()
    chart_gen.generate_all(results)
    print("[OK] Visualization complete")

def generate_report(results):
    """Generate performance report"""
    print("\nGenerating performance report...")
    report_gen = ReportGenerator()
    report_path = report_gen.create_report(results)
    print(f"[OK] Report saved to {report_path}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Hardware Performance Benchmarking Tool")
    parser.add_argument("--no-charts", action="store_true", help="Skip chart generation")
    parser.add_argument("--no-report", action="store_true", help="Skip report generation")
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    # Run benchmarks
    start_time = time.time()
    results = run_benchmarks()
    end_time = time.time()
    
    print(f"\nBenchmarking completed in {end_time - start_time:.2f} seconds")
    
    # Generate visualizations
    if not args.no_charts:
        try:
            visualize_results(results)
        except Exception as e:
            print(f"[ERROR] Visualization failed: {e}")
    
    # Generate report
    if not args.no_report:
        try:
            generate_report(results)
        except Exception as e:
            print(f"[ERROR] Report generation failed: {e}")
    
    print("\nBenchmarking process completed successfully!")

if __name__ == "__main__":
    main()
