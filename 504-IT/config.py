"""
Configuration settings for the hardware benchmarking tool
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Benchmark settings
CPU_INTENSITY_LEVELS = ["light", "medium", "heavy"]
MEMORY_SIZES = [5, 20]  # MB - reduced from [10, 100, 500]
PARALLEL_TASK_SIZES = [500, 2000]  # Reduced from [1000, 10000, 100000]
PARALLEL_THREAD_COUNTS = [2, 4]  # Reduced from [1, 2, 4, 8]

# Chart settings
CHART_DPI = 300
CHART_STYLE = "default"

# Report settings
REPORT_TEMPLATE = """
Hardware Performance Benchmark Report
=====================================

Generated: {timestamp}

System Information:
- OS: {os_name}
- CPU: {cpu_name}
- CPU Cores: {cpu_cores}
- Total Memory: {total_memory} GB

CPU Benchmark Results:
{cpu_results}

Memory Benchmark Results:
{memory_results}

Parallel Processing Results:
{parallel_results}

Summary:
{summary}
"""
