import os
import random
import re
import sys

import numpy as np

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
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
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

    # Set the random walk variable and fill dictionary
    random_walk = (1 - damping_factor)/len(corpus)
    model_dict = {page: random_walk for page in corpus.keys()}

    # check if page has links if no links add every page probability
    if len(corpus[page]) != 0:
        link_walk = (damping_factor/len(corpus[page]))
    else:
        link_walk = damping_factor/len(corpus)

    # if links exist add their probability on
    for link in corpus[page]:
        model_dict[link] += link_walk

    return model_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # create an empty rank model counter
    rank_model = {page: 0 for page in corpus.keys()}

    # begin by selecting a random page
    random_page = random.choice(list(corpus.keys()))

    # load the transition values
    transistion_dict = {page: transition_model(corpus, page, damping_factor)
                        for page in corpus.keys()}

    for _ in range(n):
        # count pages landed on
        rank_model[random_page] += 1

        # select the correct transition model
        transistion_model_ = transistion_dict[random_page]

        # select a page at random by
        # indexing the first element of the returned list
        random_page = random.choices(
            list(transistion_model_.keys()),
            weights=transistion_model_.values(),
            k=1)[0]

    # divide each value by n to normalize
    return {key: value / n for key, value in rank_model.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize N, intial model, and random walk probability
    N = len(corpus)
    iterate_model = {page: 1/N for page in corpus.keys()}
    random_walk_pr = (1-damping_factor) / N

    # continue updating until estimates converge
    while True:
        # create an empty dictionary for new probabilities
        tmp_model = {page: 0 for page in corpus.keys()}

        # update each page estimate
        # by summing up the probablities of pages that link to it
        for page in corpus.keys():
            page_pr = sum(
                damping_factor * iterate_model[p] / len(links)
                for p, links in corpus.items()
                if page in links)

            # add probabilities into the model
            tmp_model[page] = page_pr + random_walk_pr

        # check to see if values have converged
        # then return the model
        if np.allclose(
            list(tmp_model.values()),
            list(iterate_model.values()),
                atol=1e-03):

            # normalize the percentages and return
            norm = sum(iterate_model.values())
            return {p: v / norm for p, v in iterate_model.items()}

        # update the iterate_model
        iterate_model = tmp_model


if __name__ == "__main__":
    main()
