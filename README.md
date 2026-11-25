# Python Lab - Scenario Question Solutions

Solutions to the scenario-based questions from the course question sheet
(15 experiments, 10 scenario questions each, 150 in total).

**Every question is solved in its own separate section and its own separate
file.** Nothing is merged into a single combined answer.

Each experiment page below contains, per question:

- the scenario as given in the question sheet
- the rubric points it has to cover, and where the code covers them
- the complete solution code
- the real captured output of running that code

---

## Experiments

| # | Unit | Topic | Questions | Page |
|---|------|-------|-----------|------|
| 1 | I | OOP fundamentals: classes, encapsulation, inheritance, polymorphism, magic methods | 10 | [open](exp01/README.md) |
| 2 | I | Composition, abstraction, decorators, generators, iterators, closures | 10 | [open](exp02/README.md) |
| 3 | I | Generators, closures and design patterns (Singleton, Factory, Observer, Strategy) | 10 | [open](exp03/README.md) |
| 4 | II | Introduction to dynamic programming and list-based data analysis | 10 | [open](exp04/README.md) |
| 5 | II | Dynamic programming: knapsack, LIS/LCS, house robber, memoisation | 10 | [open](exp05/README.md) |
| 6 | II | 2D dynamic programming: grid paths, matrix chain, sequence alignment, edit distance | 10 | [open](exp06/README.md) |
| 7 | III | Regular expressions: extracting and validating email addresses | 10 | [open](exp07/README.md) |
| 8 | III | File handling: reading files, counting lines, writing summaries | 10 | [open](exp08/README.md) |
| 9 | III | Command-line arguments, 2D arrays and CSV to JSON conversion | 10 | [open](exp09/README.md) |
| 10 | IV | NumPy: arrays, aggregation, axis operations, boolean filtering, matrix algebra | 10 | [open](exp10/README.md) |
| 11 | IV | Pandas: Series, DataFrames, groupby, pivot tables, time series | 10 | [open](exp11/README.md) |
| 12 | IV | Pandas with Matplotlib: statistics, outliers and visualisation | 10 | in progress |
| 13 | V | Concurrency and parallelism: threading, multiprocessing, asyncio, the GIL | 10 | in progress |
| 14 | V | Logging: levels, handlers, formatters, configuration, decorators | 10 | in progress |
| 15 | V | Memory management and garbage collection: profiling, refcounts, gc | 10 | in progress |

---

## Running the programs

Python 3.10 or newer.

```bash
# experiments 1 to 9 need nothing beyond the standard library
python exp01/q1_student_record_system.py

# experiments 10 to 12 need the scientific stack
pip install numpy pandas matplotlib
python exp10/q1_marks_numpy.py
```

Notes on how the programs are written:

- **Nothing prompts you.** Scripts that would normally ask for input fall back
  to demo data when no input is available, so each file runs start to finish on
  its own.
- **Input files are created automatically.** The regex and file-handling
  experiments write their own sample `data/` files on first run, so there is no
  missing-file error.
- **Command-line scripts have defaults.** Experiment 9 uses `argparse`; every
  flag has a sensible default, and each file's docstring shows the full command
  with real arguments.
- **Random data is seeded.** Where a scenario says "generate random data", the
  seed is fixed, so the output in these pages is reproducible.
- **Charts are written to files.** Experiment 12 uses the Matplotlib `Agg`
  backend and saves PNGs into `exp12/plots/`, so nothing needs a display.

---

## A note on two repeated questions in the source sheet

The question sheet repeats a few scenarios. These solutions do not copy and
paste the earlier answer:

- **Experiment 6 Question 1** repeats Experiment 5 Question 1 (fitness band
  heart rate). The Experiment 6 version answers the same rubrics using the
  `statistics` module and a different data layout.
- **Experiment 11 Questions 2 to 10** repeat Experiment 10 Questions 2 to 10
  verbatim. Experiment 10 is the NumPy experiment and Experiment 11 is the
  Pandas experiment, so the Experiment 11 solutions answer the same scenarios
  with `Series`, `DataFrame`, `groupby` and `pivot_table` instead of raw arrays.
  Each affected file says so at the top.

---

## Repository layout

```
exp01/ .. exp15/
  README.md                 the submission page for that experiment
  q1_*.py .. q10_*.py       one file per scenario question
  data/                     sample input and output files (exp07, exp08, exp09)
  plots/                    generated charts (exp12)
```
