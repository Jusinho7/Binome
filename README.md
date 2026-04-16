*This project has been created as part of the 42 curriculum by srasolov, frazanak.*

# Push_Swap

## Description

`push_swap` is a 42 School sorting project written in C. Its purpose is to sort a list of integers using only two stacks (`stack A` and `stack B`) and a limited set of stack operations. The main goal is to produce a valid sorting sequence while minimizing the number of operations.

> **What is a stack?**
> A stack is a data structure that works like a pile of plates: you can only place or remove a plate from the top. The last element added is the first to be removed. This is known as the **LIFO** principle (Last In, First Out).

The program reads integers from the command line. It validates the input, detects duplicate values and out-of-range integers, and applies one of several stack-based algorithms to generate a sequence of operations. The output is a plain list of moves that sorts the numbers in ascending order in `stack A`.

## Instructions

### Compilation

Compile the project with the provided `Makefile`:

```bash
make
```

This command builds the `push_swap` executable using the system C compiler (`cc`) and the flags `-Wall -Wextra -Werror`.

Supported Makefile targets:

```bash
make         # build push_swap
make clean   # remove object files
make fclean  # remove object files and push_swap executable
make re      # rebuild from scratch
```

### Dependencies

This project does not require external libraries beyond the standard C toolchain. It uses a custom `ft_printf` implementation included in the repository that supports file descriptors for flexible output redirection.

### Running the Program

Use `push_swap` with numbers separated by spaces:

```bash
./push_swap 3 2 1
```

Or pass a single quoted string of numbers:

```bash
./push_swap "3 2 1"
```

Additional flags:

- `--bench`: enables benchmark output printed to standard error after the operation list
- `--adaptive`: choose the algorithm automatically (default)
- `--simple`: force the simple sorting strategy
- `--medium`: force the medium sorting strategy
- `--complex`: force the complex sorting strategy

Example with benchmark mode:

```bash
./push_swap --bench 4 2 1 3
```

### Output

The program prints the list of stack operations to standard output. Each operation is one of the allowed commands:

- `sa`, `sb`, `ss`
- `pa`, `pb`
- `ra`, `rb`, `rr`
- `rra`, `rrb`, `rrr`

If input validation fails, the program writes `Error` to standard error and exits.

## Features

- Adaptive algorithm selection based on input size and disorder
- Multiple algorithm modes: simple, medium, complex
- Input validation for:
  - non-numeric values
  - integer overflow outside `INT_MIN`..`INT_MAX`
  - duplicate integers
  - empty or blank input strings
- Benchmark mode with operation counts and strategy classification
- Support for both separate arguments and a single quoted argument string
- Robust argument parsing that ignores empty or whitespace-only arguments

## Algorithms and Justification

The project uses three sorting strategies. The chosen algorithm is either explicitly forced by a flag or selected automatically using `detect_algo()`.

### Simple Sort

- Used when the input has 5 or fewer elements, or when adaptive selection decides the list is nearly sorted.
- Implementation:
  - Find the minimum value in `stack A`
  - Rotate `stack A` or reverse-rotate it until the minimum is on top
  - Push the minimum to `stack B`
  - Repeat until `stack A` has 2 or 3 elements
  - Sort the remaining 2 or 3 elements with direct stack moves
  - Push elements back from `stack B` to `stack A`

- Complexity:
  - Worst-case time: O(n²)
  - Reason: each minimum search and rotation is O(n), and it is repeated for up to n elements

- Why chosen:
  - Best for very small lists where simple selection and minimal moves are easier to optimize
  - Avoids overhead from ranking or chunking

- Trade-offs:
  - Not efficient for large input sizes
  - Easy to implement and reliably produces a low operation count on small arrays

### Medium Sort

- Used for moderately disordered lists where adaptive selection finds a disorder ratio between 20% and 50%.
- Implementation:
  - Compute a chunk size using `ceil(sqrt(n))`
  - Create a rank array for every value in `stack A`
  - Move values in rank order from `stack A` to `stack B` chunk by chunk
  - For each chunk, if a value belongs to the current range, push it to `stack B`; otherwise rotate `stack A`
  - After all chunks are pushed, move values back from `stack B` to `stack A`, bringing the maximum in `stack B` to the top before each push

- Complexity:
  - Estimated operation complexity: O(n√n)
  - Reason: the algorithm uses roughly √n chunks and processes each remaining element with O(1) stack operations per step
  - Note: ranking uses an O(n²) pass once, which is acceptable for the expected medium range

- Why chosen:
  - Balances simplicity and performance for medium-sized inputs
  - Reduces the number of costly operations compared to a pure O(n²) method

- Trade-offs:
  - Requires rank computation and chunk management
  - Better than simple sort for moderate input sizes, but less scalable than radix-based sorting

### Complex Sort

- Used when the input is very disordered or when the `--complex` flag is forced.
- Implementation:
  - Convert each value to its rank among all values (`get_ranks()`)
  - Replace stack values with their ranks to normalize the range to `0..n-1`
  - Perform radix sort on the rank values using binary digits
  - For each bit position, push values with bit=0 to `stack B` and rotate values with bit=1 in `stack A`
  - After each bit pass, push all values back from `stack B` to `stack A`
  - Restore the original values after the sort completes

- Complexity:
  - Radix phase: O(n log n)
  - Rank conversion phase: O(n²) due to pairwise comparisons while building ranks
  - Overall: O(n² + n log n), but the main sorting phase is radix-based

- Why chosen:
  - Radix sort is a strong fit for integer sorting with stack operations because it avoids direct comparisons and uses only allowed stack moves
  - Rank compression prevents large or negative values from affecting bit-based grouping

- Trade-offs:
  - Ranking uses extra memory and O(n²) preprocessing
  - Still effective when the primary cost is measured in stack operations rather than CPU comparisons

### Adaptive Strategy

The adaptive mode chooses the algorithm automatically using `detect_algo()`:

- `n <= 5` → `SIMPLE`
- `disorder < 0.20` → `SIMPLE`
- `0.20 <= disorder < 0.50` → `MEDIUM`
- `disorder >= 0.50` → `COMPLEX`

Disorder is measured as the ratio of inversion count to the maximum number of inversions. This gives a numeric assessment of how far the list is from being sorted.

## Project Structure

- `main.c` — argument parsing, flag handling, bench mode, sort execution
- `push_swap.h` — shared types, function declarations, and core structures
- `check_files.c` — numeric parsing, range checking, duplicate detection
- `checker.c` — argument parsing utilities, flag cleanup, blank-string handling
- `check_flag.c` — algorithm selection and adaptive detection
- `search_flag.c` — command line flag scanning and removal
- `sort.c` — top-level sorter dispatch
- `sort_simple.c` — simple sorting strategy for small inputs
- `sort_medium.c` / `sort_medium_utils.c` — chunk-based medium strategy
- `sort_complex.c` / `sort_complex_utils.c` — radix-based complex strategy
- `push.c`, `swap.c`, `rotate.c`, `reverse.c` — stack operations
- `bench.c` — benchmarking output and strategy labels
- `ft_printf.*` — custom printf implementation used by the project
- `ft_split.c`, `ft_strcmp.c` — utility functions for parsing and string comparison
- `utils.c` — error handling, list freeing, and helper functions

## Usage Examples

Sort a small list:

```bash
./push_swap 2 1 3
```

Force medium mode:

```bash
./push_swap --medium 9 1 8 2 7 3
```

Use adaptive mode with benchmark output:

```bash
./push_swap --bench 5 2 8 4 1
```

Sort from a quoted string:

```bash
./push_swap "12 4 99 3"
```

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


### AI Usage in This Project

AI tools were used to assist with development and documentation:

- **Tools Used:** GitHub Copilot (for code suggestions and debugging), Claude AI and ChatGPT (for explanations and optimization ideas).
- **Tasks:** Debugging complex sorting logic, generating code snippets for edge cases, explaining algorithm concepts, drafting documentation like this README, and helping with code refactoring to meet 42 School norms.
- **Impact:** Helped accelerate problem-solving and ensure clarity, but all final code and decisions were reviewed and implemented by the developers. AI served as a supportive tool, not a replacement for manual coding.


## Limitations

- Only supports 32-bit signed integers (`INT_MIN`..`INT_MAX`)
- Invalid input prints `Error` and exits without partial output
- Does not include a separate `checker` executable target; all logic is compiled into `push_swap`
- The complex sorting strategy includes a rank mapping pass that is O(n²), so the real runtime is influenced by both preprocessing and stack operation counts
- Code follows 42 School norms: functions limited to 25 lines maximum and 4 parameters maximum

## Notes

- The benchmark mode prints detailed statistics to standard error, while the sort operations remain on standard output.
- If the input is already sorted, the program exits without printing any operations.
- The implementation has been optimized for robustness, including improved argument parsing and file descriptor support in printf functions.
