import itertools

from multiprocessing import Pool

import config
import helpers.singleton as singleton

from helpers.tools import *
from helpers.tools import ColorOutput as co
from data.gene_set import GENES_SET


def pool_action(args):
    gene = args[0]
    comb = args[1]
    for c in comb:
        cross_res = Genetics().cross_breeding(gene, c)
        for ii in cross_res:
            is_wanted = Genetics().is_wanted_any_gene(ii)
            if is_wanted:
                return gene, c, Genetics().cross_breeding(gene, c), is_wanted
    return False


@singleton.singleton
class Genetics(object):

    def __init__(self):
        self.wanted_any_genes = config.wanted_genes
        self.genes = set()

    def add(self, gene):
        self.genes.add(gene)

    def cross_breeding(self, center, surround):
        def split_res(data):
            for idx, gene_set in enumerate(data):
                for pos, gene in enumerate(gene_set):
                    if len(gene) > 1:
                        data.append([data[idx][_i][:] for _i in range(6) if _i != pos])
                        data[-1].insert(pos, [gene[1]])
                        del data[idx][pos][1]
            result = set()
            for line in data:
                line = ''.join([_i[0] for _i in line])
                result.add(line)
            return result

        if len(surround) > 8:
            print("Max surround count is 8.")
            sys.exit()
        res = []
        for i in range(6):
            genes_value = GENES_SET.copy()
            for gene in genes_value.keys():
                genes_value[gene] = 0
            genes_value[center[i]] += GENES_SET[center[i]]
            for gene in surround:
                genes_value[gene[i]] += GENES_SET[gene[i]]
            max_val = 0
            for value in genes_value.values():
                if max_val < value:
                    max_val = value
            res_g = []
            for k, v in genes_value.items():
                if v == max_val:
                    res_g.append(k)
            if len(res_g) > 1 and center[i] in res_g:
                res_g = [center[i]]
            res.append(res_g)
        return split_res([res])

    def is_wanted_gene(self, gene, wanted_gene):
        genes_set = GENES_SET.copy()
        for g in genes_set.keys():
            genes_set[g] = 0
        for g in gene:
            genes_set[g] += 1
        wanted_genes_set = GENES_SET.copy()
        for g in wanted_genes_set.keys():
            wanted_genes_set[g] = 0
        for g in wanted_gene:
            wanted_genes_set[g] += 1
        for g in gene:
            if genes_set[g] != wanted_genes_set[g]:
                return False
        return True

    def is_wanted_any_gene(self, gene):
        for wanted in self.wanted_any_genes:
            if self.is_wanted_gene(gene, wanted):
                return wanted
        return False

    def tryhard(self):
        print(f'{co.underline("Genes set:")} {{{", ".join(map(co.gene, self.genes))}}}')
        data_set = []
        for pos, gene in enumerate(self.genes):
            genes_set = [list(self.genes)[i] for i in range(len(self.genes)) if i != pos]
            for i in range(1, 9):
                comb = itertools.combinations(genes_set, i)
                data_set.append([gene, comb])
        p = Pool()
        out = [o for o in p.map(pool_action, data_set) if o and len(o[2]) <= 8]
        out = sorted(out, key=lambda i: len(i[2]))
        for w in self.wanted_any_genes:
            print()
            print(f'{co.underline("Wanted gene:")} "{co.gene(w)}"')
            min_res_genes_count = min([len(i[2]) for i in out]) if len(out) else 0
            o = [o for o in out if o[3] == w and len(o[2]) == min_res_genes_count]
            min_slaves_count = min([len(i[1]) for i in o]) if len(o) else 0
            o = [_o for _o in o if len(_o[1]) == min_slaves_count and not self.is_wanted_gene(_o[0], w)]
            if len(o):
                o = o[:1]
                print_list([f'Master gene: "{co.gene(i[0])}" Slave genes: {{{", ".join(map(co.gene, i[1]))}}} Result '
                            f'genes: {{{", ".join(map(co.gene, i[2]))}}}' for i in o])
            else:
                print('No result.')
        return False
