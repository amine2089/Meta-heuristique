# Méta-Heuristique - Traveling Salesman Problem (TSP) Solver

A comprehensive Python project implementing various meta-heuristic algorithms to solve the Traveling Salesman Problem (TSP) for 20 Algerian cities, with Algiers as the starting and ending point.

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Description](#problem-description)
- [Algorithms Implemented](#algorithms-implemented)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Details](#algorithm-details)
- [Results Visualization](#results-visualization)
- [File Format](#file-format)

## 🎯 Overview

This project implements and compares multiple meta-heuristic algorithms to solve the TSP, finding the shortest route that visits all 20 Algerian cities exactly once and returns to Algiers. Each algorithm is visualized with different colored paths on a map.

## 📊 Problem Description

The Traveling Salesman Problem (TSP) is a classic optimization problem where:
- **Objective**: Find the shortest possible route that visits each city exactly once and returns to the starting city
- **Constraint**: Must start and end at Algiers
- **Distance**: Euclidean distance between cities (in kilometers)
- **Cities**: 20 Algerian cities (wilayas)

## 🔬 Algorithms Implemented

The project includes the following meta-heuristic algorithms:

1. **Random Search** 🔵
   - Generates random paths and keeps the best one
   - Simple baseline algorithm

2. **Local Search** 🟢
   - Starts with a random solution
   - Iteratively improves by swapping two random cities
   - Accepts only improving moves

3. **Multi-Start Local Search** 🟣
   - Runs Local Search multiple times from different starting points
   - Returns the best solution found across all runs

4. **Hill Climbing** 🩷
   - Systematically explores all possible neighbor solutions
   - Moves to the best neighbor at each iteration
   - Stops when no better neighbor exists (local optimum)

5. **Simulated Annealing** ⚪
   - Accepts worse solutions with decreasing probability
   - Uses temperature parameter to escape local optima
   - Temperature decreases over time

6. **Tabu Search** 🟡
   - Maintains a memory of recently visited solutions
   - Prevents cycling back to recent solutions
   - Explores multiple neighbors per iteration

7. **Genetic Algorithm** 🟠
   - Population-based evolutionary algorithm
   - Uses crossover, mutation, and selection operators
   - Maintains diversity through generations

## 📁 Project Structure

```
Méta-Heuristique/
│
├── Representation.py          # Main script to run all algorithms and visualize results
├── the_algorithmes.py         # Contains all algorithm implementations
├── README.md                  # This file
└── algeria_20_cities_xy.csv  # Input data file (required)
```

## 📦 Requirements

- Python 3.7+
- NumPy
- Matplotlib
- Pandas

## 🔧 Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install numpy matplotlib pandas
```

3. Ensure you have the data file `algeria_20_cities_xy.csv` in the correct location, or update the file path in `Representation.py` (line 19)

## 🚀 Usage

Simply run the main script:

```bash
python Representation.py
```

This will:
1. Load the city coordinates from the CSV file
2. Calculate the distance matrix between all cities
3. Display a map of all cities
4. Run all 7 algorithms sequentially
5. Display visualizations for each algorithm with different colors
6. Print the best path and distance found by each algorithm

### Customizing Parameters

You can modify algorithm parameters in `Representation.py`:

```python
# Example: Change number of iterations for Random Search
path_Random, distance_Random = Random_Search(Distance_Matrix, nbr_villes, algiers_Index, 10000)

# Example: Change mutation rate for Genetic Algorithm
GA_path, GA_distance = Genetic_Algorithm(Distance_Matrix, nbr_villes, algiers_Index, 0.02, 40, 200)
# Parameters: mutation_rate=0.02, population_size=40, generations=200
```

## 📖 Algorithm Details

### Random Search
- **Complexity**: O(n × iterations)
- **Best for**: Baseline comparison
- **Parameters**: `num_iterations`

### Local Search
- **Complexity**: O(n² × iterations)
- **Best for**: Quick improvements from random start
- **Parameters**: `num_iterations`

### Multi-Start Local Search
- **Complexity**: O(n² × iterations × num_starts)
- **Best for**: Finding better solutions by exploring multiple regions
- **Parameters**: `num_starts`, `local_iterations`

### Hill Climbing
- **Complexity**: O(n² × iterations)
- **Best for**: Systematic local optimization
- **Parameters**: `nbr_itérations`
- **Note**: Can get stuck in local optima

### Simulated Annealing
- **Complexity**: O(n² × iterations)
- **Best for**: Escaping local optima
- **Parameters**: `nbr_itération`
- **Cooling schedule**: Exponential (α = 0.9995)

### Tabu Search
- **Complexity**: O(n² × iterations × num_neighbors)
- **Best for**: Avoiding cycling and exploring solution space
- **Parameters**: `nbr_iterations`
- **Features**: Tabu list with aspiration criteria

### Genetic Algorithm
- **Complexity**: O(n² × population_size × generations)
- **Best for**: Population-based exploration
- **Parameters**: `mutation_rate`, `population_size`, `generations`
- **Operators**: 
  - Crossover: Order crossover (OX)
  - Mutation: Random swap
  - Selection: Roulette wheel
  - Elitism: Keeps best individual

## 🎨 Results Visualization

Each algorithm produces a visualization showing:
- **Red dots**: City locations
- **Colored lines**: The path found by the algorithm
- **City labels**: Names of each city
- **Title**: Algorithm name

Color coding:
- 🔵 Blue: Random Search
- 🟢 Green: Local Search
- 🟣 Purple: Multi-Start Local Search
- 🩷 Pink: Hill Climbing
- ⚪ Silver: Simulated Annealing
- 🟡 Gold: Tabu Search
- 🟠 Orange: Genetic Algorithm

## 📄 File Format

The input CSV file should have the following format:

```csv
city,lat,lon,x_km,y_km
Algiers,36.7538,3.0588,0,0
Oran,35.6973,-0.6337,...
...
```

Where:
- `city`: City name
- `lat`: Latitude
- `lon`: Longitude
- `x_km`: X coordinate in kilometers
- `y_km`: Y coordinate in kilometers

## 📝 Notes

- All paths start and end at Algiers (index 0 is always Algiers)
- Distance calculation uses Euclidean distance
- The path is closed (returns to starting city)
- Each algorithm may produce different results due to randomness

## 🔍 Comparing Results

After running the script, compare the printed distances to see which algorithm performs best for your specific problem instance. Generally:
- **Random Search**: Usually worst (baseline)
- **Local Search**: Quick improvement
- **Multi-Start Local Search**: Better than single Local Search
- **Hill Climbing**: Good local optimization
- **Simulated Annealing**: Good balance of exploration/exploitation
- **Tabu Search**: Good for avoiding local optima
- **Genetic Algorithm**: Good for diverse exploration



