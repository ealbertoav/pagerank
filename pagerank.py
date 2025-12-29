import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+[^>]*?href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    distribution = {}

    # Get the links from the current page
    links = corpus[page]

    # Special case: if a page has no outgoing links, treat as linking to all pages
    if not links:
        links = set(corpus.keys())

    num_links = len(links)

    # Calculate probability for each page
    for p in corpus:
        # Base probability from random jump (1 - damping_factor)
        distribution[p] = (1 - damping_factor) / num_pages

        # Add probability from the following a link (damping_factor)
        if p in links:
            distribution[p] += damping_factor / num_links

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to a transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize count for each page
    page_counts = {page: 0 for page in corpus}

    # Get a list of all pages for random selection
    pages = list(corpus.keys())

    # Generate the first sample uniformly at random
    current_page = random.choice(pages)
    page_counts[current_page] += 1

    # Generate remaining n-1 samples
    for _ in range(n - 1):
        # Get transition probabilities from the current page
        distribution = transition_model(corpus, current_page, damping_factor)

        # Select the next page based on transition probabilities
        pages_list = list(distribution.keys())
        probabilities = list(distribution.values())
        current_page = random.choices(pages_list, weights=probabilities, k=1)[0]
        page_counts[current_page] += 1

    # Convert counts to proportions
    pagerank = {page: count / n for page, count in page_counts.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)

    # Initialize each page with rank 1/N
    pagerank = {page: 1 / num_pages for page in corpus}

    # Precompute which pages link to each page, handling pages with no links
    # A page with no links is treated as linking to all pages
    links_to = {page: set() for page in corpus}
    for page in corpus:
        outgoing_links = corpus[page]
        if not outgoing_links:
            # Page with no links is treated as linking to all pages
            for target in corpus:
                links_to[target].add(page)
        else:
            for link in outgoing_links:
                links_to[link].add(page)

    # Precompute the number of links for each page (for the formula)
    num_links = {}
    for page in corpus:
        if corpus[page]:
            num_links[page] = len(corpus[page])
        else:
            # Page with no links is treated as linking to all pages
            num_links[page] = num_pages

    # Iterate until convergence
    converged = False
    while not converged:
        new_pagerank = {}
        converged = True

        for page in corpus:
            # Calculate a new rank using PageRank formula
            # PR(p) = (1-d)/N + d * sum(PR(i)/NumLinks(i)) for all i that link to p
            rank = (1 - damping_factor) / num_pages

            # Sum contributions from all pages that link to this page
            for linking_page in links_to[page]:
                rank += damping_factor * pagerank[linking_page] / num_links[linking_page]

            new_pagerank[page] = rank

            # Check if this page's rank changed by more than 0.001
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False

        pagerank = new_pagerank

    return pagerank


if __name__ == "__main__":
    main()
