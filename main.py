import os
import time
import datetime

import config

from genes_db import GenesDB
from genetics import Genetics
from helpers.tools import *
from helpers.tools import ColorOutput as co

commands = {
    'create': {'parameter': 'database_name', 'description': "Create database"},
    'stop': {'parameter': '', 'description': "Stop program"},
    'add': {'parameter': 'gene_set', 'description': "Add gene set to database"},
    'delete': {'parameter': 'database_name', 'description': "Delete database"},
    'wipe': {'parameter': 'database_name', 'description': "Wipe database"},
    'remove': {'parameter': 'gene_set', 'description': "Remove gene from database"},
    'get_all': {'parameter': '', 'description': "Print all genes from database"},
    'rand': {'parameter': 'count', 'description': "Add random gene set"},
    'action': {'parameter': '', 'description': "Run crossbreeding search"},
    'help': {'parameter': '', 'description': "Help command"}
}

last_log = 'data/last.log'


def create(args):
    if len(args) != 2:
        print(f"{co.red('Missing required parameter:')} <{co.bold(commands['create']['parameter'])}>")
        return False
    name = args[1]
    GenesDB(name)
    with open(last_log, 'w') as f:
        f.write(name)
    print(co.green('Done!'))
    return True


def delete(args):
    if len(args) != 2:
        print(f"{co.red('Missing required parameter:')} <{co.bold(commands['delete']['parameter'])}>")
        return False
    GenesDB(args[1]).delete_db()
    if os.path.exists(config.last_log_file):
        os.remove(config.last_log_file)
    print(co.green('Done!'))
    return True


def wipe(args):
    name = GenesDB().name
    GenesDB().delete_db()
    GenesDB(name)
    print(co.green('Done!'))
    return True


def add(args):
    if len(args) != 2:
        print(f"{co.red('Missing required parameter:')} <{co.bold(commands['add']['parameter'])}>")
        return False
    genes = args[1]
    GenesDB().add(genes)
    if config.insta_calculate:
        action(None)
    print(co.green('Done!'))
    return True


def remove(args):
    if len(args) != 2:
        print(f"{co.red('Missing required parameter:')} <{co.bold(commands['remove']['parameter'])}>")
        return False
    genes = args[1]
    GenesDB().remove(genes)
    print(co.green('Done!'))
    return True


def get_all(args):
    print(f'{{{", ".join(map(co.gene, [i[1] for i in GenesDB().get_all()]))}}}')
    return True


def rand(args):
    if len(args) != 2:
        print(f"{co.red('Missing required parameter:')} <{co.bold(commands['remove']['parameter'])}>")
        return False
    GenesDB().rand_data(args[-1])
    print(co.green('Done!'))
    return True


def stop(args):
    sys.exit()


def action(args):
    BEFORE = time.perf_counter()
    Genetics().genes = []
    for i in GenesDB().get_all():
        Genetics().add(i[1])
    print(co.yellow("Calculating... May take a long time if many inputs genes."))
    Genetics().tryhard()
    print(co.green(f'Done! {datetime.timedelta(seconds=round(time.perf_counter() - BEFORE))}'))
    return True


def help(args):
    for command, items in commands.items():
        print(f'{co.yellow(command)} {co.blue(items["parameter"])} {co.underline(items["description"])}')


def main():
    if not config.colored_output:
        bcolors().disable()
    if os.path.exists(config.last_log_file):
        with open(config.last_log_file, 'r') as f:
            name = f.readline()
            GenesDB(name)
            print(f'{co.yellow("Connected to database")} '
                  f'{co.yellow(f"{GenesDB().filename_start}/{GenesDB().name}{GenesDB().filename_end}")}')
    print(f"Type {co.yellow('help')} for see available commands.")
    print("Enter command:")
    try:
        while True:
            i = input()
            if i.split()[0] not in commands.keys():
                print(co.yellow(f'Command <{i}> not found.'))
                continue
            globals()[i.split()[0]](i.split())
    except KeyboardInterrupt as e:
        print(co.blue("Exit."))


if __name__ == '__main__':
    main()
