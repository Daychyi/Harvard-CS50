"""
Project 2
CS50's Introduction to Artificial Intelligence with Python
https://cs50.harvard.edu/ai/2023/

Attempted by
Daychyi Ku
https://github.com/Daychyi

"""

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
    
    pages = list(corpus.keys())
    page_prob = {}

    if page in corpus:
        # equal probability for all pages in corpus
        page_prob = {k:(1-damping_factor)/len(pages) for k in pages}

        # add probability from current page
        page_links = list(corpus[page])
        page_prob.update({k:v+(damping_factor/len(page_links)) \
                        for (k,v) in page_prob.items() if k in page_links})
        
    else: #current page not in corpus, use all pages in corpus
        page_prob = {k:1/len(pages) for k in pages}
            
    sample = random.choices(pages,list(page_prob.values()), k=1)
    
    return page_prob, sample
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # print(f"corpus:{corpus}")

    prev_sample = []
    current_sample = []
    sample = []
    pages = list(corpus.keys())
    
    # n=1000000
    for i in range(n):
        if i==0:
            current_sample = [random.choice(pages)]
            page_prob = {k:1/len(pages) for k in pages}
        else:
            page_prob, current_sample = transition_model(corpus, prev_sample, damping_factor)
            
        prev_sample = current_sample[0]
        sample.append(current_sample[0])
        
    # print(f"sample:{sample}")
    # print(f"pages:{pages}")
    return {k:sample.count(k)/n for k in pages}
    # raise NotImplementedError

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # print(f"corpus:{corpus}")

    pages = list(corpus.keys())
    page_rank_i = {k:1/len(pages) for k in pages} #initialization
    
    while(True):
        page_rank_p = iterate_page(corpus, damping_factor, page_rank_i)
        # print(f"page_rank_p:{page_rank_p}")
        # print(f"sum: {sum(list(page_rank_p.values()))}")
        diff = 0
        for p in page_rank_p:
            diff += abs(page_rank_p[p] - page_rank_i[p])
        if diff < 0.001: #update is less than 0.001
            break
        page_rank_i = page_rank_p
        
    return page_rank_p
    # raise NotImplementedError

def iterate_page(corpus, damping_factor, page_rank):
    page_p = {}
    page_number = len(list(corpus.keys()))
    
    for page in page_rank:
        pr_i = 0
        page_key = [k for (k,v) in corpus.items() if page in v]
        # print(f"page_key:{page_key}")
        for p in page_key:
            pr_i += page_rank[p]/len(corpus[p])
        page_p[page] = (1-damping_factor)/page_number + \
                    damping_factor * pr_i

    return page_p


if __name__ == "__main__":
    main()
