from datetime import datetime
from itertools import chain
from block import Block
from random import randint
from collections import Counter
from flask import jsonify, request
import random

import uuid

class Blockchain:
    
    def __init__(self):
        self.MAX_WITNESS_ALLOWED  = 2
        self.transactions = []
        self.chain = []
        self.delegates = [] #nodess who will participate in the voting process
        self.users = {} # key=UserID and value=name
        self.property = {} # key=PropertyID and value=owner
        self.nodes = {} # key=IP:Port and value=stake
        self.witnesses = [] # For ease of use we will maintain only 2 witnesses at a time
        
        genesis_block = Block(len(self.chain) + 1, [], 0)
        self.chain.append(genesis_block)        
        self.add_node('127.0.0.1:5000', 10)
        self.witnesses.append(5000)
    
    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, sellerID, buyerID, propertyID):
        # if buyerID not in self.users:
        #     return "buyerID is not registered"

        # if sellerID not in self.users:
        #     return "sellerID is not registered"
        
        #if propertyID not in property:
        #    return "proprtyID is not registered"
        
        #if property[propertyID] is not sellerID:
        #   return "Proprty ID " + propertyID + " is not registed with the seller ID " + sellerID 
        
        self.transactions.append({
            'sellerID' : sellerID,
            'buyerID' : buyerID,
            'propertyID' : propertyID,
            'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        for t in self.transactions:
            print(t)
        return "Transaction successfully added"
    
    def add_user(self, name):
        id = uuid.uuid4().hex
        self.users[id] = name
        return id

    def add_property(self, ownerID, propertyID):
        #if propertyID in property:
        #    return "Property ID already registered with " + self.user[self.property[propertyID]]
        self.property[propertyID] = ownerID
        return "Property added"
    
    def add_node(self, socket, stake):
        self.nodes[socket] = stake
        return self.nodes

    def new_block(self, prev_hash=None):   
        print('Crearting new block...')
        prev_hash = self.last_block.my_hash #['merkleRoot']
        b = Block(len(self.chain) + 1, self.transactions, prev_hash)
        self.chain.append(b)
        self.transactions = []
        return len(self.chain)

    def add_delegate(self, socket):
        if socket not in self.nodes:
            return "nodes with Socket " + socket + " not present"        
        self.delegates.append(socket)
        return "Delegate Added"
            
    def simulate_votes(self):
        simulated_votes = []
        n = len(self.nodes)
        w = [int(x) / 100 for x in self.nodes.values()]
        for _ in range (n):
            simulated_votes.append(random.choices(list(self.nodes.keys()), weights=w, k=1)[0])
        return simulated_votes
     
    def initiate_voting(self):
        votes = Counter(self.simulate_votes())
        self.witnesses = votes.most_common(self.MAX_WITNESS_ALLOWED)
        return self.witnesses

    # verifies the hashes of the blocks in the chain 
    def is_chain_valid(self, chain):
        current_block = chain[0]
        next_block_index = 1

        while next_block_index < len(chain):
            block = chain[next_block_index]

            if block['my_hash'] != current_block['prev_hash']:
                return False
            
            current_block = block
            next_block_index += 1

        return True

    def get_transaction_history(self, propertyID):
        #only check the ones that have made it into the blockchain
        transaction_history = []
        for b in self.chain:
            for t in b.transactions:
                    if t['propertyID'] == propertyID:
                        transaction_history.append(t)
        
        return transaction_history

    #Method to replace the blockchain with the longest validated chain in the network.
    def resolve_chain(self):
        neighbours = self.witnesses
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours: 
            response = request.get(f'http://{node}/chain')
        
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
        
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    new_chain = chain
        
        if new_chain:
            self.chain = new_chain
            return True

        return False
    
    def get_local_blockchain(self):
        response = []
        for b in self.chain:
            response.append(b.to_json())
        return response
    
    




    



