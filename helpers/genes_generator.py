import random

GENES = 'YGHXW'
REDS = 'XW'


def random_gene(max_reds=2):
    while True:
        g = ''.join([GENES[random.randrange(5)] for i in range(6)])
        c = 0
        for i in g:
            if i in REDS:
                c += 1
        if c > max_reds:
            continue
        return g


def random_gene_set(count=random.randint(3, 30)):
    return [random_gene() for i in range(count)]


if __name__ == '__main__':
    print(random_gene_set())
