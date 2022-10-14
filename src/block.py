from datetime import datetime
import json
import uuid
from typing import List
import hashlib


class Block:
    # def __init__(self, index, transactions, prev_hash):
    #     self.index = index,
    #     self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
    #     self.transactions = transactions,
    #     transaction_list = json.dumps(transactions)
    #     self.prev_hash = prev_hash,
    #     self.merkleRoot = MerkleTree.createMerkleTree(transaction_list)  
    #     self.print_block()      

    def __init__(self, index, transactions,prev_hash):
        self.index = index,
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        self.transactions = transactions
        self.merkleRoot = MerkleTree.createMerkleTree(transactions)
        self.my_hash = self.generate_hash(self.index, self.timestamp, self.merkleRoot)
        self.prev_hash = prev_hash
        #self.print_block()
    
    def to_json(self):
        json_block = {
            'index' : self.index,
            'timestamp' : self.timestamp,
            'transactions' : self.transactions,
            'merkleRoot' : self.merkleRoot,
            'my_hash' : self.my_hash,
            'prev_hash' : self.prev_hash
        }
        return json_block

    def generate_hash(self, index, timestamp, merkleRoot) -> str:
        return Node.hash(str(index) + str(timestamp) + str(merkleRoot))

    def myHash(self):
        if not self.merkleRoot:
            self.createMerkleTree(self.transactions)
        else:
            self.merkleRoot
    
    
    def print_block(self):
        print('block ID', self.index)
        print('block transactions', self.transactions)
        print('block hash', self.merkleRoot)
        return

    # Merkle Tree code

class Node:
    def __init__(self, left, right, value: str, content, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def __str__(self):
        return (str(self.value))

    def copy(self):
        """
        class copy function
        """
        return Node(self.left, self.right, self.value, self.content, True)

# Feature 4 - Implementation of Merkle root to calculate the hash of all the transactions in a block.
class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.__buildTree(values)

    def __buildTree(self, values: List[str]) -> None:

        leaves: List[Node] = [Node(None, None, Node.hash(e), e)
                              for e in values]
        if len(leaves) % 2 == 1:
            # duplicate last elem if odd number of elements
            leaves.append(leaves[-1].copy())
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            # duplicate last elem if odd number of elements
            nodes.append(nodes[-1].copy())
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Node(left, right, value, content)

    def getRootHash(self) -> str:
        return self.root.value


    def createMerkleTree(transactions) -> str:        
        elems = json.dumps(transactions)
        if len(elems) > 1:
            mtree = MerkleTree(elems)
            return mtree.getRootHash()


    #def createMerkleTree(self, transactions):
    #    return random.random()
