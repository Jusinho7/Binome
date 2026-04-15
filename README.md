*This project has been created as part of the 42 curriculum by srasolov, frazanak.*

# Push_Swap

## Description

Push_swap is a sorting algorithm project from the 42 School curriculum. The goal is to **sort a list of integers** using only **two stacks** (called **stack A** and **stack B**) and a limited set of predefined operations.

> **What is a stack?**
> A stack is a data structure that works like a pile of plates: you can only place or remove a plate from the top. The last element added is the first to be removed. This is known as the **LIFO** principle (Last In, First Out).

Unlike standard sorting where you can use built-in sort functions, here you must **implement the sorting logic yourself** using only basic stack manipulation operations.

The program receives a list of integers as input and outputs a sequence of operations that, when applied in order, will sort the numbers **in ascending order in stack A**. The challenge is to find the shortest possible sequence — fewer operations means better performance.

---

## Instructions

### Compilation

Use the provided Makefile to compile the project:

```bash
make
```

This command reads the `Makefile` (a kind of build script) and generates the `push_swap` executable.

> **What is a Makefile?**
> It's a file that contains instructions to automate the compilation of your C code. Instead of manually typing long `gcc` commands, you simply type `make` and it handles everything for you.

---

### Running the Program

Once compiled, run the program by passing integers as arguments:

```bash
./push_swap [numbers]
```

For example:

```bash
./push_swap 3 2 1
```

> **How to read this command?**
> - `./push_swap` — runs the program located in the current directory
> - `3 2 1` — the numbers to sort, separated by spaces
>
> The program will print in the terminal the list of operations needed to sort those numbers.

---

### Counting Operations with `wc -l`

To measure your algorithm's efficiency, you can count how many operations are generated:

```bash
./push_swap 3 2 1 | wc -l
```

> **How does this command work?**
> - `|` is called a "pipe". It redirects the output of one command into the input of another.
> - `wc -l` counts the number of lines in the text it receives.
> - Combined, they count how many operations `push_swap` generated.
> - The smaller this number, the more efficient your algorithm is!

---

## Algorithms

The project implements **three main sorting strategies**, automatically selected based on the size of the input. This adaptive selection ensures the program stays efficient regardless of how much data it receives.

---

### Simple Sort (O(n²))

- **For what input size?** Small lists (typically up to 5–6 numbers).
- **How does it work?** It uses a **selection sort** approach:
  1. Find the smallest element in stack A.
  2. Rotate it to the top of the stack.
  3. Push it to stack B.
  4. Repeat until stack A is empty.
  5. Push everything back to stack A.
- **Why this choice?** For tiny lists, simplicity wins. There's no need for complex logic when sorting only 5 numbers.
- **Time complexity:** O(n²) — acceptable for small n.

> **What is O(n²)?**
> It's a notation that measures how the number of operations grows relative to the input size. O(n²) means that if you double the number of elements, the number of operations is multiplied by 4. Fine for small lists, but slow for large ones.

---

### Medium Sort (O(n√n))

- **For what input size?** Medium lists (roughly 6 to 100 numbers).
- **How does it work?** It uses a **hybrid approach**:
  1. Divide the stack into several **chunks** of similar size.
  2. Sort within each chunk using rotations and pushes to stack B.
  3. Merge the chunks back to rebuild a sorted list in stack A.
- **Why this choice?** This is a good middle ground — more efficient than simple sort for medium lists, without the overhead of more complex algorithms.
- **Time complexity:** O(n√n) — a solid balance between simplicity and performance.

> **What is O(n√n)?**
> It sits between O(n²) and O(n log n). For example, for 100 elements: n√n ≈ 1,000 operations, compared to 10,000 for O(n²). A significant improvement!

---

### Complex Sort (O(n log n))

- **For what input size?** Large lists (100+ numbers).
- **How does it work?** It uses **radix sort** or a similar bit-level technique:
  1. Examine numbers bit by bit (right to left in binary representation).
  2. For each bit, distribute elements into the two stacks based on the bit value (0 or 1).
  3. Repeat for each significant bit.
- **Why this choice?** Highly efficient for large datasets. Radix sort is stable and performs very well with integers within the constraints of a stack-based system.
- **Time complexity:** O(n log n) — optimal for sorting algorithms.

> **What is O(n log n)?**
> For 1,000 elements: n log n ≈ 10,000 operations, versus 1,000,000 for O(n²). This is one of the most efficient complexities achievable for a sorting algorithm.

The adaptive selection ensures the program always performs well: small inputs use simple methods, while large ones leverage advanced techniques.

---

## Features

- **Error Handling:** The program validates input and reports any errors:
  - Duplicate numbers in the list
  - Non-numeric values (e.g. letters)
  - Integer overflow (numbers too large or too small for an `int`)
  - On any error, the program prints `Error` to the standard error output.

- **Optimized Operations:** Algorithms are designed to minimize unnecessary moves, reducing the total operation count.

- **Benchmark System:** Use the `--bench` flag to display detailed performance statistics after sorting (see examples below).

---

## Usage Examples

### Basic Sorting

```bash
$ ./push_swap 3 2 1
pb
sa
pa
```

> 💡 **What happens step by step?**
> - Initial stack A: `[3, 2, 1]` (3 is on top)
> - `pb` — push 3 from A to B → A: `[2, 1]`, B: `[3]`
> - `sa` — swap the top two elements of A → A: `[1, 2]`, B: `[3]`
> - `pa` — push 3 from B back to A → A: `[1, 2, 3]`
>
> Stack A is now sorted in ascending order (1 on top, 3 on bottom) in just 3 operations!

---

### With Benchmark Mode

```bash
$ ./push_swap --bench 4 2 1 3
pb
pb
sa
pa
pa
[bench] disorder:   75.00%
[bench] strategy:   Simple / O(n²)
[bench] total_ops:  5
[bench] sa: 1  sb: 0  ss: 0  pa: 2  pb: 2
[bench] ra: 0  rb: 0  rr: 0  rra: 0
[bench] rrb: 0  rrr: 0
```

> 💡 **How to read this report?**
> - `disorder: 75.00%` — the initial list was 75% out of order. The higher this percentage, the harder it is to sort.
> - `strategy: Simple / O(n²)` — the algorithm automatically selected (Simple sort here, since there are only 4 numbers).
> - `total_ops: 5` — only 5 operations were needed to sort the list.
> - `sa: 1, pa: 2, pb: 2` — a breakdown of how many times each operation was used.

---

### Counting Operations

```bash
$ ./push_swap 1 5 2 4 3 | wc -l
12
```

Here, 12 operations were needed to sort the list `[1, 5, 2, 4, 3]`.

---

## Resources

### Useful Links

- [Stack Data Structure](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) — To understand how a stack works.
- [Sorting Algorithms Overview](https://en.wikipedia.org/wiki/Sorting_algorithm) — To explore the different sorting strategies that exist.
- [Radix Sort Explanation](https://en.wikipedia.org/wiki/Radix_sort) — To understand in detail the radix sort algorithm used for large lists.

---

##  Work Distribution

This project was developed as a pair, with clearly defined responsibilities to maximize efficiency and maintain code quality throughout the development process.

---

###  srasolov — Infrastructure & Tooling

Responsible for the foundation that makes the algorithms run — data structures, input handling, and tooling:

- Built the stack data structures and all core operations:
  - `push`, `swap`, `rotate`, `reverse rotate` (for both stacks)
- Developed robust input parsing and validation:
  - Duplicate detection, non-numeric input rejection, integer overflow protection
- Engineered the benchmark system (`--bench` flag):
  - Per-operation counters (`sa`, `pb`, `ra`, etc.)
  - Disorder percentage calculation and performance display
- Contributed to testing pipelines and debugging sessions

---

###  frazanak — Algorithms & Optimization

Responsible for the core intelligence of the program — everything related to how numbers actually get sorted:

- Designed and implemented all three sorting strategies:
  - **Simple Sort** — selection-based approach for small inputs
  - **Medium Sort** — chunk-based hybrid strategy for medium inputs
  - **Radix Sort** — bit-level sorting for large inputs
- Tuned each algorithm to minimize the total number of operations
- Led performance analysis and testing strategies
- Investigated and resolved complex algorithmic edge cases

---

###  Shared Responsibilities

Beyond their individual domains, both members collaborated on:

- Algorithm design decisions and strategy selection logic
- Code review, refactoring, and maintaining code standards
- Edge case testing and validation
- Writing this documentation
- Norminette

> Good code is rarely written alone. Every major decision in this project was discussed, reviewed, and validated by both contributors.

---

### AI Usage in This Project

AI tools were used to assist with development and documentation:

- **Tools Used:** GitHub Copilot (for code suggestions and debugging) and ChatGPT (for explanations and optimization ideas).
- **Tasks:** Debugging complex sorting logic, generating code snippets for edge cases, explaining algorithm concepts, and drafting documentation like this README.
- **Impact:** Helped accelerate problem-solving and ensure clarity, but all final code and decisions were reviewed and implemented by the developers. AI served as a supportive tool, not a replacement for manual coding.

