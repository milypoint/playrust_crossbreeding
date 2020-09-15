import os
import sqlite3

from helpers.singleton import Singleton
from data.gene_set import GENES_SET
from helpers.tools import *
from helpers.genes_generator import random_gene_set


class GenesDB(object, metaclass=Singleton):

    filename_start = 'data'
    filename_end = '.sqlite'

    def __init__(self, name=None):
        if not hasattr(self, 'name') and name is None:
            print('Parameter <name> is missing.')
            type(self.__class__)._instances = {}
            del self
            return
        self.name = name
        self.file = f"{self.filename_start}/{self.name}{self.filename_end}"
        self.db_init()

    def db_init(self):
        if not os.path.exists(self.filename_start):
            os.makedirs(self.filename_start)
        if os.path.exists(f"{self.file}"):
            file_exists = True
        else:
            file_exists = False
        self.conn = sqlite3.connect(f'./{self.file}')
        self.cursor = self.conn.cursor()
        if not file_exists:
            sql_create_table = """
            CREATE TABLE IF NOT EXISTS list (
            id integer PRIMARY KEY,
            genes text NOT NULL
            );
            """
            sql_create_idx_list_genes = """CREATE UNIQUE INDEX idx_list_genes ON list(genes);"""
            self.cursor.execute(sql_create_table)
            self.cursor.execute(sql_create_idx_list_genes)
        self.conn.commit()

    def get_all(self):
        sql = """SELECT * FROM list"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add(self, genes):
        genes = genes.upper()
        if not self.validate(genes):
            print("Genes data not valid.")
            return False
        sql = """INSERT INTO list(genes) VALUES(?)"""
        try:
            self.cursor.execute(sql, [genes])
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"{genes} already exists.")
        return True

    def remove(self, genes):
        genes = genes.upper()
        if not self.validate(genes):
            print("Genes data not valid.")
            return False
        sql = """SELECT id FROM list WHERE genes=?"""
        self.cursor.execute(sql, [genes])
        row = self.cursor.fetchall()
        if len(row) == 0:
            print(f"Gene {genes} not found.")
            return False
        else:
            sql = """DELETE FROM list WHERE id=?"""
            self.cursor.execute(sql, row[0])
            self.conn.commit()
            print('Done!')
            return True

    def delete_db(self):
        if os.path.exists(self.file):
            self.conn.close()
            os.remove(self.file)
            print(f"{self.file} removed.")
            type(self.__class__)._instances = {}
            del self
        else:
            print(f"File {self.file} not exists.")

    def validate(self, genes):
        if len([g for g in genes if g.upper() in GENES_SET]) != 6:
            return False
        else:
            return True

    def rand_data(self, count=None):
        for i in random_gene_set(int(count)):
            self.add(i)
