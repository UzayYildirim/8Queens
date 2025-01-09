# 8 Queens Problem, using Genetic Algorithms

How to place 8 chess queens on a chessboard provided that no two queens threaten each other?

(2 queens must not be on the same row, column, or diagonal.)

The 8 Queens Problem was first proposed by the chess player **Max Bezzel** in 1848. It was later studied by mathematicians like Gauss and Georg Cantor. The first solution was presented by Franz Nauck in 1850, thus formalizing the problem.

The maximum number of queens that can be placed on an *n x n* chessboard, where no two queens threaten each other, is equal to *n*. One of the classic combinatorial problems is placing eight queens on an 8 x 8 chessboard, where no two queens threaten each other (i.e., they cannot attack each other). This problem has been generalized for *n* queens, where no queens can attack each other. The latest known solution is for *n = 26*. A solution for *n = 27* has not yet been found, as it requires significant computational power.

Multiple methods exist for solving the 8 Queens Problem, such as Brute Force, Genetic Algorithms, Hill Climbing, Random Walk, and GBF/A methods. There are 96 distinct solutions for an 8x8 chessboard.

### Chessboard Solution Example

|   | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 1 | Q |   |   |   |   |   |   |   |
| 2 |   |   |   |   | Q |   |   |   |
| 3 |   | Q |   |   |   |   |   |   |
| 4 |   |   |   |   |   |   | Q |   |
| 5 |   |   |   | Q |   |   |   |   |
| 6 |   |   |   |   |   |   |   | Q |
| 7 |   |   | Q |   |   |   |   |   |
| 8 |   |   |   |   |   | Q |   |   |

---

## Single Point Crossover

A point is selected in the parent array. All data beyond this point in the array is swapped between the two parents. Crossover points are selected by considering **Positional Bias**.

### Single Point Crossover Example

#### Parent Chromosomes
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Parent A | 5 | 6 | 3 | 4 | 7 | 2 | 8 | 1 |
| Parent B | 3 | 4 | 7 | 8 | 1 | 5 | 6 | 2 |

#### Crossover Point: 4

- **Explanation**: The crossover point is chosen at position 4, splitting each parent chromosome into two segments: the first part is preserved, while the remaining segments are swapped between the parents. This ensures the new chromosomes inherit traits from both parents in a structured way.

#### Offspring Chromosomes
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Offspring 1 | 5 | 6 | 3 | 4 | 1 | 5 | 6 | 2 |
| Offspring 2 | 3 | 4 | 7 | 8 | 7 | 2 | 8 | 1 |

---

## Two Point Crossover

This is a special case of the N-point Crossover technique. Two points are randomly selected on the chromosomes, and genetic material is exchanged at these points.

### Two Point Crossover Example

#### Parent Chromosomes
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Parent A | 1 | 5 | 3 | 4 | 6 | 2 | 8 | 7 |
| Parent B | 4 | 2 | 8 | 7 | 3 | 6 | 5 | 1 |

#### Crossover Points: 3, 6

- **Explanation**: Two points are selected at positions 3 and 6. The sections between these two points in the chromosomes are swapped. This provides additional diversity to the offspring compared to a single-point crossover, as it allows two distinct parts of the chromosome to be combined.

#### Offspring Chromosomes
| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|----------|---|---|---|---|---|---|---|---|
| Offspring 1 | 1 | 5 | 3 | 7 | 3 | 6 | 8 | 7 |
| Offspring 2 | 4 | 2 | 8 | 4 | 6 | 2 | 5 | 1 |

---

## Solution of 8 Queens Problem Using Genetic Algorithm

1. **Population Initialization**: The population size is determined by the board size, and the initial population is generated randomly.
2. **Evaluation**: Chromosome candidates are evaluated for fitness.
3. **Selection**: Chromosomes with better fitness scores are selected for the next generation.
4. **Crossover**: A single or double-point crossover (based on user input) is applied to generate offspring.
5. **Mutation**: A mutation operator is applied to the offspring.
6. **Iteration**: The process repeats until a generation with queens that do not attack each other is found, or the maximum number of iterations is reached.

---

## Experiment and Results

In this study, two different techniques were experimented with: the **Single Point Crossover** and **Two Point Crossover** methods. The goal was to determine which of these techniques is more effective in solving the 8 Queens Problem using genetic algorithms.

### Conditions for the experiment:
**For a choice of 8 board size:**
- **CPU**: Intel(R) Core(TM) i5-8300H CPU @ 2.30GHz
- **OS**: Windows 10 Pro 21H2 (Build Number 19044.1706)
- **CPU Architecture**: 64-Bit (x86-64)
- **Python Version**: Python 3.10
- **Amount of RAM allocated for Python**: 12GB
- **NumPy Library Version**: numpy-1.22.4-cp310-cp310-win_amd64.whl

**For a choice of 16 board size:**
- **CPU**: AMD Ryzen 9 5950X 16-Core CPU @ 3.40GHz
- **OS**: Windows Server 2019
- **CPU Architecture**: 64-Bit (x86-64)
- **Python Version**: Python 3.10
- **Amount of RAM allocated for Python**: 3GB
- **NumPy Library Version**: numpy-1.22.4-cp310-cp310-win_amd64.whl

The maximum iteration value for all tests was set to 2000.  
Mutation functionality was used in all tests.

---

# Results:

## Board 8 Data

| Trial | Crossover Type | Iteration Count |
|-------|----------------|-----------------|
| 1     | 1              | 157             |
| 2     | 1              | 45              |
| 3     | 1              | 121             |
| 4     | 1              | 197             |
| 5     | 1              | 241             |
| **Average (1)** |        | **152.20**     |
| 1     | 2              | 680             |
| 2     | 2              | 335             |
| 3     | 2              | 227             |
| 4     | 2              | 433             |
| 5     | 2              | 114             |
| **Average (2)** |        | **357.80**     |

## Board 16 Data

| Trial | Crossover Type | Iteration Count |
|-------|----------------|-----------------|
| 1     | 1              | 930             |
| 2     | 1              | 1342            |
| 3     | 1              | 1642            |
| 4     | 1              | 1837            |
| 5     | 1              | 1011            |
| **Average (1)** |        | **1352.40**    |
| 1     | 2              | 1903            |
| 2     | 2              | Timeout         |
| 3     | 2              | 1885            |
| 4     | 2              | 1475            |
| 5     | 2              | 1983            |
| **Average (2)** |        | **1811.50**    |


- For the **8 board size**, the **Single Point Crossover** technique yielded better results, completing the process with fewer iterations and higher success rates compared to the **Two Point Crossover** technique.
- Similarly, for the **16 board size**, the **Single Point Crossover** method outperformed the Two Point Crossover in terms of efficiency and effectiveness.

**As a result, it has been determined that the Single Point Crossover technique gives better results for the 8 Queens Problem. To reach this conclusion, each test was repeated at least five times for both crossover types.**
