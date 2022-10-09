from datetime import datetime
from itertools import chain
from block import Block
import random

import uuid

class Blockchain:
    
    def __init__(self):
        self.transactions = []
        self.chain = []
        self.users = dict() # key=UserID and value=name
        self.property = dict() # key=PropertyID and value=owner
        self.peer = dict() # key=IP:Port and value=stake
        genesis_block = Block(len(self.chain) + 1, self.transactions, 0)
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, sellerID, buyerID, propertyID):
        self.transactions.append({
            'SellerID' : sellerID,
            'BuyerID' : buyerID,
            'PropertyID' : propertyID,
            'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        #TODO - code to check if the seller buyer and property are registered with the system
        for t in self.transactions:
            print(t)
        return True
    
    def add_user(self, name):
        id = uuid.uuid4().hex
        self.users[id] = name
        return id

    def add_property(self, ownerID, propertyID):
        self.users[propertyID] = ownerID
        return True
    
    def add_peer(self, socket, stake):
        self.peer[socket] = stake
        return self.peer

    def new_block(self, prev_hash=None):   
        print('Crearting new block...')
        prev_hash = self.last_block.my_hash #['my_hash']
        b = Block(len(self.chain) + 1, self.transactions, prev_hash)
        self.chain.append(b)
        self.transactions = []
        return len(self.chain)



