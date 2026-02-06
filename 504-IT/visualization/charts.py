"""
Chart generation for benchmark results
"""

import os
import matplotlib.pyplot as plt
from config import RESULTS_DIR, CHART_DPI, CHART_STYLE

class ChartGenerator:
    """Generate charts from benchmark results"""
    
    def __init__(self):
        try:
            plt.style.use(CHART_STYLE)
        except:
            plt.style.use('default')
        self.results_dir = RESULTS_DIR
        os.makedirs(self.results_dir, exist_ok=True)
    
    def generate_cpu_chart(self, cpu_results):
        """Generate CPU performance chart"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Integer operations
            ops_sec = cpu_results["integer_ops"]["operations_per_second"]
            ax1.bar(["Integer Ops"], [ops_sec], color='skyblue')
            ax1.set_ylabel('Operations per Second')
            ax1.set_title('CPU Integer Performance')
            ax1.set_ylim(0, ops_sec * 1.2)
            
            # Floating point operations
            sizes = ["Small (50)", "Medium (150)"]
            flops = [
                cpu_results["floating_point_ops_small"]["flops"],
                cpu_results["floating_point_ops_medium"]["flops"]
            ]
            
            ax2.bar(sizes, flops, color='lightcoral')
            ax2.set_ylabel('FLOPS')
            ax2.set_title('CPU Floating Point Performance')
            ax2.set_ylim(0, max(flops) * 1.2)
            
            plt.tight_layout()
            chart_path = os.path.join(self.results_dir, "cpu_performance.png")
            plt.savefig(chart_path, dpi=CHART_DPI)
            plt.close()
            
            print(f"[OK] CPU chart saved: {chart_path}")
            return chart_path
        except Exception as e:
            print(f"[ERROR] CPU chart failed: {e}")
            return None
    
    def generate_memory_chart(self, mem_results):
        """Generate memory performance chart"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            
            # Sequential access
            seq_data = {k: v for k, v in mem_results.items() if "sequential_access" in k}
            if seq_data:
                labels = [f"{v['size_mb']}MB" for v in seq_data.values()]
                values = [v["bandwidth_mb_per_sec"] for v in seq_data.values()]
                ax.bar(labels, values, color='lightgreen')
                ax.set_ylabel('MB/sec')
                ax.set_title('Sequential Memory Access Performance')
                ax.set_ylim(0, max(values) * 1.2)
            
            plt.tight_layout()
            chart_path = os.path.join(self.results_dir, "memory_performance.png")
            plt.savefig(chart_path, dpi=CHART_DPI)
            plt.close()
            
            print(f"[OK] Memory chart saved: {chart_path}")
            return chart_path
        except Exception as e:
            print(f"[ERROR] Memory chart failed: {e}")
            return None
    
    def generate_parallel_chart(self, parallel_results):
        """Generate execution time line graph: sequential vs parallel execution"""
        try:
            # Extract data for each task size
            task_sizes = {}
            for key, result in parallel_results.items():
                task_size = result.get("task_size")
                if task_size:
                    if task_size not in task_sizes:
                        task_sizes[task_size] = {"sequential": None, "threading": {}, "multiprocessing": {}}
                    
                    if "sequential_" in key:
                        task_sizes[task_size]["sequential"] = result["time_seconds"]
                    elif "threading_" in key:
                        thread_count = result.get("thread_count")
                        if thread_count:
                            task_sizes[task_size]["threading"][thread_count] = result["time_seconds"]
                    elif "multiprocessing_" in key:
                        process_count = result.get("process_count")
                        if process_count:
                            task_sizes[task_size]["multiprocessing"][process_count] = result["time_seconds"]
            
            if not task_sizes:
                return None
            
            # Use largest task size for visualization
            max_task_size = max(task_sizes.keys())
            data = task_sizes[max_task_size]
            
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Plot sequential baseline
            if data["sequential"]:
                ax.axhline(y=data["sequential"], color='red', linestyle='--', linewidth=2.5, label='Sequential Execution')
            
            # Plot threading execution times
            if data["threading"]:
                thread_counts = sorted(data["threading"].keys())
                thread_times = [data["threading"][tc] for tc in thread_counts]
                ax.plot(thread_counts, thread_times, marker='o', linewidth=2.5, markersize=10, label='Threading (Multi-threaded)', color='green')
            
            # Plot multiprocessing execution times
            if data["multiprocessing"]:
                process_counts = sorted(data["multiprocessing"].keys())
                process_times = [data["multiprocessing"][pc] for pc in process_counts]
                ax.plot(process_counts, process_times, marker='s', linewidth=2.5, markersize=10, label='Multiprocessing (Multi-core)', color='blue')
            
            ax.set_xlabel('Number of CPU Cores / Threads', fontsize=12, fontweight='bold')
            ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
            ax.set_title(f'Execution Time: Sequential vs Parallel Execution\n(Task Size: {max_task_size} primes)', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=11, loc='best')
            
            # Set x-axis ticks
            all_cores = sorted(set((list(data["threading"].keys()) if data["threading"] else []) + 
                                   (list(data["multiprocessing"].keys()) if data["multiprocessing"] else [])))
            if all_cores:
                ax.set_xticks(all_cores)
            
            plt.tight_layout()
            chart_path = os.path.join(self.results_dir, "parallel_execution_time.png")
            plt.savefig(chart_path, dpi=CHART_DPI)
            plt.close()
            
            print(f"[OK] Parallel execution time chart saved: {chart_path}")
            return chart_path
        except Exception as e:
            print(f"[ERROR] Parallel chart failed: {e}")
            return None
    
    def generate_all(self, results):
        """Generate all charts from benchmark results"""
        try:
            print("[OK] Generating charts...")
            cpu_chart = self.generate_cpu_chart(results["cpu"])
            mem_chart = self.generate_memory_chart(results["memory"])
            parallel_chart = self.generate_parallel_chart(results["parallel"])
            print(f"[OK] All charts saved to {self.results_dir}")
            return {"cpu": cpu_chart, "memory": mem_chart, "parallel": parallel_chart}
        except Exception as e:
            print(f"[ERROR] Chart generation failed: {e}")
            return {}
