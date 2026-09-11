import csv
import sys
import itertools

PROBS = {
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {
            True: 0.65, #P(trait = True|gene = 2)
            False: 0.35
        },
        1: {
            True: 0.56,
            False: 0.44
        },
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    "mutation": 0.01
}

def main():
    if len(sys.argv) != 2:
        sys.exit("use-> py heredity.py data.csv")

    people = load_data(sys.argv[1])

    probabilities = {}
    for person in people:
        probabilities[person] = {           
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

    names = set(people)
    for have_trait in powerset(names):
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)

    for person in people:
        print(f"{person}: ")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}: ")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
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
    s = list(s)
    return [set(s) for s in itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s)+1)
    )]

def joint_probability(people, one_gene, two_genes, have_trait):
    p = 1
    for person in people:
        if person in one_gene:
            gene = 1
        elif person in two_genes:
            gene = 2
        else:
            gene = 0

        trait = person in have_trait

        if people[person]["mother"] is None and people[person]["father"] is None:
            probability = PROBS["gene"][gene]
            trait_probability = PROBS["trait"][gene][trait]
            p = p * probability * trait_probability
        else:
            mother = people[person]["mother"]
            father = people[person]["father"]

            if mother in one_gene:
                m_pass = 0.5
            elif mother in two_genes:
                m_pass = 0.99
            else:
                m_pass = 0.01

            if father in one_gene:
                p_pass = 0.5
            elif father in two_genes:
                p_pass = 0.99
            else:
                p_pass = 0.01

            if gene == 1:
                probability = (1 - p_pass) * m_pass + (1 - m_pass) * p_pass
            elif gene == 0:
                probability = (1 - p_pass) * (1 - m_pass)
            else:
                probability = p_pass * m_pass

            trait_probability = PROBS["trait"][gene][trait]
            p = probability * p * trait_probability
    return p 

def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        if person in one_gene:
            gene = 1
        elif person in two_genes:
            gene = 2
        else: 
            gene = 0

        probabilities[person]["gene"][gene] += p

        trait = person in have_trait
        probabilities[person]["trait"][trait] += p

def normalize(probabilities):
    for person in probabilities:
        gene_total = 0
        trait_total = 0
        for i in range(3):
            gene_total += probabilities[person]["gene"][i]            
        for trait in [True, False]:
            trait_total += probabilities[person]["trait"][trait]
        for i in range(3):
            probabilities[person]["gene"][i] /= gene_total
        for trait in [True, False]:
            probabilities[person]["trait"][trait] /= trait_total

if __name__ == "__main__":
    main()