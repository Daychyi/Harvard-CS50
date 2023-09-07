"""
Project 2
CS50's Introduction to Artificial Intelligence with Python
https://cs50.harvard.edu/ai/2023/

Attempted by
Daychyi Ku
https://github.com/Daychyi

"""

import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    
    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # print(f"2:{two_genes},\t 1:{one_gene},\t trait:{have_trait}")
    p = 1.0

    for person in people:
        gene_count = 0
        trait_status = False
        if person in have_trait: 
            trait_status = True
        if person in two_genes: #person has 2 gene 
            gene_count = 2
        elif person in one_gene: #person has 1 gene 
            gene_count = 1

        p *= person_prob(people, person, one_gene, two_genes, gene_count)
        p *= PROBS['trait'][gene_count][trait_status]

        # print(f"joint_probability: {p}")
    return p
    # raise NotImplementedError

def person_prob(people, person, one_gene, two_genes, gene_count):
    """ return probability of a person with gene_count"""
    
    mom = people[person]['mother']
    dad = people[person]['father']

    if mom is None: #without parent
        return PROBS["gene"][gene_count]

    else: # get genes from parents
        gene_from_dad = gene_from_parent_prob(dad,one_gene,two_genes)#1 gene from dad
        gene_from_mom = gene_from_parent_prob(mom,one_gene,two_genes)#1 gene from mom

        match gene_count: 
            case 2: # the person has 2 gene
                return gene_from_dad * gene_from_mom

            case 1: # the person has 1 gene
                return gene_from_mom * (1 - gene_from_dad ) + \
                      ( 1 - gene_from_mom ) * gene_from_dad
                
            case _: # the person has 0 gene
                return (1 - gene_from_mom) * (1 - gene_from_dad)
    
    
def gene_from_parent_prob(parent, one_gene, two_genes):
    """ return the probability of a person getting 1 gene from a parent"""
    if parent in two_genes: # parent has 2 gene
        return (1 - PROBS["mutation"])
    elif parent in one_gene: # parent has 1 gene
        return 0.5
    else: # parent has 0 gene
        return PROBS["mutation"]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person in probabilities:
        probabilities[person]["trait"][person in have_trait] += p
        if person in two_genes:
            probabilities[person]["gene"][2] += p 
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else:
            probabilities[person]["gene"][0] += p
    
    # print(f"updated probabilities: {probabilities}")
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        gene_sum = sum(probabilities[person]["gene"].values())
        probabilities[person]["gene"].update( (key,value/gene_sum) for key, value \
                             in probabilities[person]["gene"].items() \
                             if gene_sum != 0 )
        
        trait_sum = sum(probabilities[person]["trait"].values())
        probabilities[person]["trait"].update( (key,value/trait_sum) for key, value \
                             in probabilities[person]["trait"].items() \
                             if trait_sum != 0 )
    # print(f"normalised prob:{probabilities}")
    # raise NotImplementedError


if __name__ == "__main__":
    main()
