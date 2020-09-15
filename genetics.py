import itertools

from multiprocessing import Pool

import config
import helpers.singleton as singleton

from helpers.tools import *
from helpers.tools import ColorOutput as co
from data.gene_set import GENES_SET


def pool_action(args):
    gene = args[0]
    combinations = args[1]
    res = []
    for combination in combinations:
        crossbreeding_result = Genetics().crossbreeding(gene, combination)
        for ii in crossbreeding_result:
            is_wanted_gene = Genetics().is_wanted_any_gene(ii)
            if is_wanted_gene:
                res.append([gene, combination, crossbreeding_result, is_wanted_gene])
    return res


@singleton.singleton
class Genetics(object):

    def __init__(self):
        self.wanted_any_genes = config.wanted_genes
        self.genes = []

    def add(self, gene):
        if gene not in self.genes:
            self.genes.append(gene)

    @staticmethod
    def crossbreeding(master, slaves):
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
            return list(result)

        def genetics_calc(master_gene, slave_genes):
            gene_values = {k: 0 for k, v in GENES_SET.copy().items()}
            for g in slave_genes:
                gene_values[g] += GENES_SET[g]
            res = [g for g, v in gene_values.items() if v == max(gene_values.values()) and v > GENES_SET[master_gene]]
            return res if len(res) else [master_gene]

        if len(slaves) > 8:
            print("Max surround count is 8.")
            sys.exit()

        res = [genetics_calc(master[i], [g[i] for g in slaves]) for i in range(6)]
        return split_res([res])

    def is_wanted_gene(self, gene, wanted_gene):
        gene_values = {k: 0 for k, v in GENES_SET.copy().items()}
        wanted_genes_values = gene_values.copy()
        for g in gene:
            gene_values[g] += 1
        for g in wanted_gene:
            wanted_genes_values[g] += 1
        for g in gene:
            if gene_values[g] != wanted_genes_values[g]:
                return False
        return True

    def is_wanted_any_gene(self, gene):
        for wanted in self.wanted_any_genes:
            if self.is_wanted_gene(gene, wanted):
                return wanted
        return False

    def tryhard(self):
        print(f'{co.underline(f"Genes set: ({len(self.genes)})")} {{{", ".join(map(co.gene, self.genes))}}}')
        data_set = []
        for pos, gene in enumerate(self.genes):
            genes_set = [self.genes[i] for i in range(len(self.genes)) if i != pos]
            for i in range(1, 9):
                comb = itertools.combinations(genes_set, i)
                data_set.append([gene, comb])
                # 50/50 method:
                if i == 2:
                    data_set.append([gene, [(gene, ) + c for c in comb]])
        p = Pool()
        out = []
        for o in p.map(pool_action, data_set):
            for _o in o:
                if len(_o) and len(_o[2]) <= 8:
                    out.append(_o)
        for w in self.wanted_any_genes:
            out_by_w = [o for o in out if o[3] == w]
            print()
            print(f'{co.underline("Wanted gene:")} "{co.gene(w)}"')
            min_res_genes_count = min([len(i[2]) for i in out_by_w]) if len(out_by_w) else 0
            o = [o for o in out_by_w if len(o[2]) == min_res_genes_count]
            min_slaves_count = min([len(i[1]) for i in o]) if len(o) else 0
            o = [_o for _o in o if len(_o[1]) == min_slaves_count and not self.is_wanted_gene(_o[0], w)]
            if len(o):
                print_list([f'Master gene: "{co.gene(i[0])}" Slave genes: {{{", ".join(map(co.gene, i[1]))}}} Result '
                            f'genes: {{{", ".join(map(co.gene, i[2]))}}} {"50/50 method" if i[0] in i[1] else ""}' for i in o])
            else:
                print('No result.')
        return False
