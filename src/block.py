from datetime import datetime
import random

class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index,
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
        self.transactions = transactions,
        self.prev_hash = prev_hash,
        self.my_hash = self.createMerkleTree(self.transactions)  
        self.print_block()      

    def myHash(self):
        if not self.my_hash:
            self.createMerkleTree(self.transactions)
        else:
            self.my_hash

    def createMerkleTree(self, transactions):
        return random.random()

    def print_block(self):
        print('block ID', self.index)
        print('block transactions', self.transactions)
        print('block hash', self.my_hash)
        return