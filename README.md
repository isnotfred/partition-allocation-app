# Partition Allocation Simulator

A Python-based GUI application that simulates fixed partition memory allocation algorithms used in operating systems. This educational tool allows users to visualize and compare different memory allocation strategies.

## Overview

The Partition Allocation Simulator demonstrates four classic memory allocation algorithms:
- **First Fit**: Allocates jobs to the first available partition that fits
- **Best Fit**: Allocates jobs to the partition with the smallest sufficient space
- **Worst Fit**: Allocates jobs to the partition with the largest sufficient space
- **Next Fit**: Similar to First Fit, but continues from the last allocation position

## Features

- **Interactive GUI**: User-friendly interface built with PyQt5
- **Dynamic Job Management**: Add jobs with custom memory requirements
- **Flexible Partition Configuration**: Create partitions of varying sizes
- **Real-time Visualization**: See allocation changes instantly
- **Multiple Algorithms**: Compare different allocation strategies
- **Job Lifecycle Management**: Track jobs from waiting → allocated → finished
- **Deallocation Support**: Free partitions and simulate job completion
- **Reset Functionality**: Clear all data and start fresh

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository:
```bash
git clone https://github.com/isnotfred/partition-allocation-app.git
cd partition-allocation-app
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- **PyQt5**: GUI framework for the application interface

See `requirements.txt` for specific versions.

## Usage

### Running the Application

```bash
python main.py
```

### Using the Simulator

1. **Add Partitions**:
   - Enter memory space in KB (e.g., 100, 200, 300)
   - Click "Add Partition"
   - Partitions appear as F1, F2, F3, etc.

2. **Add Jobs**:
   - Enter memory needed in KB (e.g., 50, 150, 250)
   - Click "Add Job"
   - Jobs appear as J1, J2, J3, etc. with "Waiting" status

3. **Allocate Jobs**:
   - Select an algorithm from the dropdown
   - Click "ALLOCATE"
   - Watch as jobs are assigned to partitions

4. **Deallocate Jobs**:
   - Select an allocated job from the dropdown
   - Click "DEALLOCATE"
   - The partition is freed and job marked as "Finished"

5. **Reset**:
   - Click "RESET" to clear all jobs and partitions
   - Start a new simulation from scratch

### Example Scenario

```
Partitions: F1(100KB), F2(200KB), F3(300KB)
Jobs: J1(80KB), J2(150KB), J3(250KB)

First Fit Result:
- F1(100KB) → J1(80KB)    [20KB wasted]
- F2(200KB) → J2(150KB)   [50KB wasted]
- F3(300KB) → J3(250KB)   [50KB wasted]

Best Fit Result:
- F1(100KB) → J1(80KB)    [20KB wasted]
- F2(200KB) → J2(150KB)   [50KB wasted]
- F3(300KB) → J3(250KB)   [50KB wasted]
```

## Project Structure

```
partition-allocation-app/
│
├── partition/                 # Core package
│   ├── __init__.py           # Package initializer
│   ├── algorithms.py         # Allocation algorithms implementation
│   └── memory_classes.py     # Partition and Job class definitions
├── .gitignore                # Git ignore rules
├── LICENCE                   # License information
├── main.py                   # GUI application entry point
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

## Algorithm Details

### First Fit
- **Strategy**: Scans partitions from the beginning
- **Pros**: Fast allocation
- **Cons**: May create fragmentation at memory start

### Best Fit
- **Strategy**: Finds partition with minimum wasted space
- **Pros**: Minimizes internal fragmentation per allocation
- **Cons**: Slower; may leave many small unusable fragments

### Worst Fit
- **Strategy**: Chooses partition with maximum remaining space
- **Pros**: Leaves larger reusable fragments
- **Cons**: May increase overall external fragmentation

### Next Fit
- **Strategy**: Continues searching from last allocation point
- **Pros**: Distributes allocations evenly; faster than First Fit
- **Cons**: May skip better fits at the beginning

## Educational Use

This simulator is ideal for:
- Operating Systems courses
- Computer Science students learning memory management
- Demonstrating internal fragmentation concepts
- Comparing algorithm efficiency and tradeoffs

## Technical Details

### Memory Management Concepts

- **Internal Fragmentation**: Wasted space within allocated partitions
- **External Fragmentation**: Free memory scattered in small blocks
- **Fixed Partitioning**: Memory divided into fixed-size blocks at system start

### Job States
- **Waiting**: Job created but not yet allocated
- **Allocated**: Job assigned to a partition
- **Finished**: Job deallocated and completed

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Frederick Orlain**
- GitHub: [@isnotfred](https://github.com/isnotfred)

## Acknowledgments

- Built with PyQt5 framework
- Inspired by operating systems course materials

## Version

* **1.0.0**

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: fredorlain5@gmail.com

---