# Hardware Performance Benchmarking Tool

A comprehensive tool for benchmarking CPU, memory, and parallel processing performance.

## Features

- CPU performance testing (integer and floating-point operations)
- Memory performance testing (sequential/random access, allocation)
- Parallel processing benchmarking (threading vs. multiprocessing)
- Automatic data generation for tests
- Visualization of results
- Report generation

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the complete benchmark suite:
```
python main.py
```

Run benchmarks without generating charts:
```
python main.py --no-charts
```

Run benchmarks without generating a report:
```
python main.py --no-report
```

## Output

- Benchmark results are saved in the `results/` directory
- Charts are saved as PNG files in the `results/` directory
- Reports are saved in the `reports/` directory

## Example Output

```
Starting hardware benchmarking suite...
Timestamp: 2023-11-15 14:30:22
--------------------------------------------------
Generating test data...

Running CPU benchmarks...

Running memory benchmarks...

Running parallel processing benchmarks...

Benchmarking completed in 125.43 seconds

Generating visualization charts...
Charts saved to results/

Generating performance report...
Report saved to reports/benchmark_report_20231115_143222.txt

Benchmarking process completed successfully!
```
