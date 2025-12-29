# PageRank

A Python implementation of Google's PageRank algorithm for ranking web pages based on their link structure.

## Background

PageRank is an algorithm developed by Google founders Larry Page and Sergey Brin to rank web pages in search engine results. The core idea is that a page is important if many other important pages link to it.

The algorithm models a "random surfer" who:
- With probability **d** (damping factor, typically 0.85): follows a random link from the current page
- With probability **1-d**: jumps to any random page in the corpus

A page's PageRank represents the probability that the random surfer ends up on that page at any given time.

## Project Structure

```
pagerank/
├── pagerank.py          # Main implementation file
├── corpus0/             # Test corpus with 4 pages
│   ├── 1.html
│   ├── 2.html
│   ├── 3.html
│   └── 4.html
├── corpus1/             # Test corpus with 7 pages (search/games themed)
│   ├── bfs.html
│   ├── dfs.html
│   ├── games.html
│   ├── minesweeper.html
│   ├── minimax.html
│   ├── search.html
│   └── tictactoe.html
└── corpus2/             # Test corpus with 8 pages (programming/AI themed)
    ├── ai.html
    ├── algorithms.html
    ├── c.html
    ├── inference.html
    ├── logic.html
    ├── programming.html
    ├── python.html
    └── recursion.html
```

## Implementation Details

### `transition_model(corpus, page, damping_factor)`

Returns a probability distribution over which page to visit next, given the current page.

**How it works:**
1. With probability `damping_factor`: randomly choose one of the links from the current page
2. With probability `1 - damping_factor`: randomly choose any page in the corpus
3. Combines both probabilities for each page in the corpus

**Special case:** If a page has no outgoing links, it's treated as if it links to all pages (including itself).

### `sample_pagerank(corpus, damping_factor, n)`

Estimates PageRank values using Monte Carlo sampling (random simulation).

**How it works:**
1. Start by choosing a random page uniformly from all pages
2. For each subsequent sample, use `transition_model` to determine the next page
3. Count how many times each page was visited across `n` samples
4. Return the proportion of visits for each page

### `iterate_pagerank(corpus, damping_factor)`

Calculates PageRank values using the iterative formula until convergence.

**How it works:**
1. Initialize all pages with rank `1/N` (where N is total number of pages)
2. Repeatedly update each page's rank using the formula:
   ```
   PR(p) = (1-d)/N + d × Σ(PR(i)/NumLinks(i))
   ```
   where the sum is over all pages `i` that link to page `p`
3. Stop when no page's rank changes by more than 0.001

**Special case:** Pages with no outgoing links are treated as linking to all pages.

## Usage Instructions

Run the program from the command line, providing a corpus directory as an argument:

```bash
python pagerank.py corpus0
```

Or with Python 3 explicitly:

```bash
python3 pagerank.py corpus0
```

### Examples

```bash
# Run with the simple 4-page corpus
python3 pagerank.py corpus0

# Run with the search/games corpus
python3 pagerank.py corpus1

# Run with the programming/AI corpus
python3 pagerank.py corpus2
```

## Requirements

- **Python 3.6+**
- Standard library only (no external dependencies)
  - `os` - File system operations
  - `random` - Random number generation
  - `re` - Regular expressions for HTML parsing
  - `sys` - Command line arguments

## Example Output

Running `python3 pagerank.py corpus0`:

```
PageRank Results from Sampling (n = 10000)
  1.html: 0.2198
  2.html: 0.4303
  3.html: 0.2183
  4.html: 0.1316
PageRank Results from Iteration
  1.html: 0.2198
  2.html: 0.4294
  3.html: 0.2198
  4.html: 0.1311
```

Note: Sampling results may vary slightly between runs due to randomness.

## Algorithm Explanation

### Sampling Method (Monte Carlo)
- **Approach:** Simulates a random surfer browsing pages
- **Pros:** Simple to implement, works well for large corpora
- **Cons:** Results vary between runs, requires many samples for accuracy
- **Accuracy:** Improves with more samples (default: 10,000)

### Iterative Method
- **Approach:** Mathematically computes exact PageRank using linear algebra
- **Pros:** Deterministic results, mathematically precise
- **Cons:** May require many iterations to converge
- **Convergence:** Stops when all ranks change by less than 0.001

Both methods should produce similar results. The iterative method gives exact values, while sampling provides estimates that converge to the true values as the number of samples increases.

## Constants

The program uses these default values (defined at the top of `pagerank.py`):

| Constant | Value | Description |
|----------|-------|-------------|
| `DAMPING` | 0.85 | Probability of following a link vs. random jump |
| `SAMPLES` | 10000 | Number of samples for the sampling method |

